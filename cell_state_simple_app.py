#!/usr/bin/env python3
"""Plain Tk desktop editor for pancreatic islet cell-state models.

The model covers a tissue (the pancreatic islet) made up of multiple cell
types (beta cell, alpha cell, ...), each with its own distinct set of gene
programs and cell states. Pick a cell type from the menu near the top to
inspect or edit that cell type's states/programs independently of the others.
"""

import copy
import json
import os
import tkinter as tk
from tkinter import filedialog, font as tkfont, messagebox, simpledialog

from cell_state_desktop import ACTIVITY_LABELS, ACTIVITY_LEVELS, ACTIVITY_VALUES, DEFAULT_MODEL, split_genes, slugify, validate_model

UI_FONT_FAMILY = "Avenir"
UI_FONT_SIZE = 11


class SimpleCellStateApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Cell State Model Editor")
        self.geometry("1150x780")
        self.minsize(980, 660)
        self.configure(bg="#f8faf8")

        self._configure_fonts()

        self.model = copy.deepcopy(DEFAULT_MODEL)
        self.file_path = None
        self.dirty = False
        self.selected_cell_type_id = self.model["cellTypes"][0]["id"]
        cell_type = self.current_cell_type()
        self.selected_state_id = cell_type["states"][0]["id"] if cell_type and cell_type["states"] else None
        self.selected_program_id = None
        self.activity_var = tk.StringVar(value="baseline")
        self.cell_type_var = tk.StringVar()

        self.make_menu()
        self.make_widgets()
        self.refresh_all()
        self.after(100, self.raise_window)

    def _configure_fonts(self):
        # Switch the widgets that use Tk's named default fonts (Entry, Button,
        # OptionMenu, Listbox, menus, etc.) over to the UI font in one place.
        for font_name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont"):
            try:
                tkfont.nametofont(font_name).configure(family=UI_FONT_FAMILY, size=UI_FONT_SIZE)
            except tk.TclError:
                pass

    def make_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="New from defaults", command=self.new_from_defaults)
        file_menu.add_command(label="Open JSON...", command=self.open_json)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Save As...", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.on_close)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def make_widgets(self):
        # NOTE: this used to lay out the header/left/right frames with .place().
        # On macOS, Tk's place() manager combined with older bundled Tcl/Tk builds
        # (8.5.x and some 8.6.9 builds) has a known bug where content inside
        # place()-managed frames never gets painted. grid()/pack() do not have
        # this problem, so the whole top-level layout uses grid() instead.
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        header_bar = tk.Frame(self, bg="#ffffff", height=54)
        header_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        header_bar.grid_propagate(False)
        self.header = tk.Label(header_bar, text="Program space", bg="#ffffff", fg="#152126", anchor="w", font=(UI_FONT_FAMILY, 16, "bold"))
        self.header.pack(side="left", fill="both", expand=True, padx=(12, 0))
        self.status = tk.Label(header_bar, text="", bg="#ffffff", fg="#647178", anchor="e", width=40)
        self.status.pack(side="right", fill="y", padx=(0, 12))

        # Tissue is made up of multiple cell types; this bar picks which
        # cell type's programs/states are shown below.
        cell_type_bar = tk.Frame(self, bg="#f8faf8")
        cell_type_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=12, pady=(8, 4))
        tk.Label(cell_type_bar, text="Cell type:", bg="#f8faf8", font=(UI_FONT_FAMILY, UI_FONT_SIZE, "bold")).pack(side="left", padx=(0, 8))
        self.cell_type_menubutton = tk.Menubutton(cell_type_bar, textvariable=self.cell_type_var, relief="raised", bg="#ffffff", padx=10, pady=3)
        self.cell_type_menu = tk.Menu(self.cell_type_menubutton, tearoff=False)
        self.cell_type_menubutton.configure(menu=self.cell_type_menu)
        self.cell_type_menubutton.pack(side="left")
        tk.Button(cell_type_bar, text="Add cell type", command=self.add_cell_type).pack(side="left", padx=(10, 0))
        tk.Button(cell_type_bar, text="Rename", command=self.rename_cell_type).pack(side="left", padx=(6, 0))
        tk.Button(cell_type_bar, text="Delete cell type", command=self.delete_cell_type).pack(side="left", padx=(6, 0))

        self.left = tk.Frame(self, bg="#f8faf8", width=285)
        self.left.grid(row=2, column=0, sticky="nsw", padx=(12, 10), pady=(4, 12))
        self.left.grid_propagate(False)
        self.right = tk.Frame(self, bg="#f8faf8")
        self.right.grid(row=2, column=1, sticky="nsew", padx=(0, 12), pady=(4, 12))

        tk.Label(self.left, text="States", bg="#f8faf8", fg="#152126", anchor="w", font=(UI_FONT_FAMILY, 12, "bold")).pack(fill="x")
        self.state_list = tk.Listbox(self.left, exportselection=False, font=(UI_FONT_FAMILY, UI_FONT_SIZE))
        self.state_list.pack(fill="both", expand=True, pady=(6, 8))
        self.state_list.bind("<<ListboxSelect>>", self.on_state_select)

        state_buttons = tk.Frame(self.left, bg="#f8faf8")
        state_buttons.pack(fill="x")
        tk.Button(state_buttons, text="Add", command=self.add_state).pack(side="left", fill="x", expand=True)
        tk.Button(state_buttons, text="Duplicate", command=self.duplicate_state).pack(side="left", fill="x", expand=True, padx=4)
        tk.Button(state_buttons, text="Delete", command=self.delete_state).pack(side="left", fill="x", expand=True)

        tk.Button(self.left, text="Add program", command=self.add_program).pack(fill="x", pady=(16, 4))
        tk.Button(self.left, text="Edit selected program", command=self.edit_selected_program).pack(fill="x")

        details = tk.LabelFrame(self.right, text="Selected state", bg="#f8faf8", fg="#152126", padx=10, pady=8)
        details.pack(fill="x")

        tk.Label(details, text="Name", bg="#f8faf8", anchor="w").grid(row=0, column=0, sticky="w")
        self.state_name = tk.Entry(details)
        self.state_name.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=3)

        tk.Label(details, text="Phenotype", bg="#f8faf8", anchor="w").grid(row=1, column=0, sticky="nw")
        self.state_phenotype = tk.Text(details, height=3, wrap="word")
        self.state_phenotype.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=3)

        tk.Button(details, text="Apply state details", command=self.apply_state_details).grid(row=2, column=1, sticky="e", pady=(6, 0))
        details.columnconfigure(1, weight=1)

        controls = tk.Frame(self.right, bg="#f8faf8")
        controls.pack(fill="x", pady=(12, 6))
        tk.Label(controls, text="Programs sorted by activity", bg="#f8faf8", font=(UI_FONT_FAMILY, 12, "bold")).pack(side="left")
        tk.Label(controls, text="Search", bg="#f8faf8").pack(side="left", padx=(24, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_args: self.refresh_program_list())
        tk.Entry(controls, textvariable=self.search_var).pack(side="left", fill="x", expand=True)

        program_area = tk.Frame(self.right, bg="#f8faf8")
        program_area.pack(fill="both", expand=True)
        self.program_list = tk.Listbox(program_area, exportselection=False, font=("Menlo", 10))
        self.program_list.pack(side="left", fill="both", expand=True)
        self.program_list.bind("<<ListboxSelect>>", self.on_program_select)
        scrollbar = tk.Scrollbar(program_area, orient="vertical", command=self.program_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.program_list.config(yscrollcommand=scrollbar.set)

        activity_bar = tk.Frame(self.right, bg="#f8faf8")
        activity_bar.pack(fill="x", pady=(8, 0))
        tk.Label(activity_bar, text="Selected program activity:", bg="#f8faf8").pack(side="left")
        tk.OptionMenu(activity_bar, self.activity_var, *[label for _value, label in ACTIVITY_LEVELS]).pack(side="left", padx=6)
        tk.Button(activity_bar, text="Apply activity", command=self.apply_activity).pack(side="left")
        self.selected_program_label = tk.Label(activity_bar, text="No program selected", bg="#f8faf8", fg="#647178", anchor="w")
        self.selected_program_label.pack(side="left", padx=12, fill="x", expand=True)

    def raise_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(400, lambda: self.attributes("-topmost", False))
        # macOS Tk (especially the system-installed Tcl/Tk 8.5/8.6.9 builds) has a
        # known bug where the window frame draws but the widgets inside stay blank
        # until the window is resized. Force a redraw by nudging the size by a
        # pixel and back.
        self.update_idletasks()
        width, height = self.winfo_width(), self.winfo_height()
        self.geometry("{}x{}".format(width + 1, height))
        self.after(50, lambda: self.geometry("{}x{}".format(width, height)))

    def current_cell_type(self):
        for cell_type in self.model["cellTypes"]:
            if cell_type["id"] == self.selected_cell_type_id:
                return cell_type
        return self.model["cellTypes"][0] if self.model["cellTypes"] else None

    def current_state(self):
        cell_type = self.current_cell_type()
        if not cell_type:
            return None
        for state in cell_type["states"]:
            if state["id"] == self.selected_state_id:
                return state
        return None

    def update_status(self):
        name = os.path.basename(self.file_path) if self.file_path else "Untitled model"
        self.status.config(text="{} ({})".format(name, "modified" if self.dirty else "saved"))

    def mark_dirty(self):
        self.dirty = True
        self.update_status()

    def refresh_all(self):
        self.refresh_cell_type_options()
        self.refresh_state_list()
        self.refresh_state_details()
        self.refresh_program_list()
        self.update_status()

    def refresh_cell_type_options(self):
        cell_types = self.model["cellTypes"]
        ids = [cell_type["id"] for cell_type in cell_types]
        if self.selected_cell_type_id not in ids:
            self.selected_cell_type_id = ids[0] if ids else None

        self.cell_type_menu.delete(0, "end")
        for cell_type in cell_types:
            self.cell_type_menu.add_command(
                label=cell_type["name"],
                command=lambda cell_type_id=cell_type["id"]: self.select_cell_type(cell_type_id),
            )

        cell_type = self.current_cell_type()
        self.cell_type_var.set(cell_type["name"] if cell_type else "No cell type")
        self.header.config(text="{} program space".format(cell_type["name"]) if cell_type else "Program space")

    def select_cell_type(self, cell_type_id):
        if cell_type_id == self.selected_cell_type_id:
            return
        self.selected_cell_type_id = cell_type_id
        cell_type = self.current_cell_type()
        self.selected_state_id = cell_type["states"][0]["id"] if cell_type and cell_type["states"] else None
        self.refresh_all()

    def add_cell_type(self):
        name = simpledialog.askstring("Add cell type", "Cell type name:", parent=self)
        if not name:
            return
        existing = {cell_type["id"] for cell_type in self.model["cellTypes"]}
        cell_type = {"id": slugify(name, existing), "name": name.strip(), "programs": [], "states": []}
        self.model["cellTypes"].append(cell_type)
        self.selected_cell_type_id = cell_type["id"]
        self.selected_state_id = None
        self.mark_dirty()
        self.refresh_all()

    def rename_cell_type(self):
        cell_type = self.current_cell_type()
        if not cell_type:
            return
        name = simpledialog.askstring(
            "Rename cell type", "Cell type name:", initialvalue=cell_type["name"], parent=self
        )
        if not name:
            return
        cell_type["name"] = name.strip()
        self.mark_dirty()
        self.refresh_all()

    def delete_cell_type(self):
        cell_type = self.current_cell_type()
        if not cell_type:
            return
        if len(self.model["cellTypes"]) == 1:
            messagebox.showerror("Cannot delete", "The model needs at least one cell type.")
            return
        if not messagebox.askyesno(
            "Delete cell type",
            "Delete '{}' and all of its programs and states?".format(cell_type["name"]),
        ):
            return
        self.model["cellTypes"] = [item for item in self.model["cellTypes"] if item["id"] != cell_type["id"]]
        self.selected_cell_type_id = self.model["cellTypes"][0]["id"]
        self.selected_state_id = None
        self.mark_dirty()
        self.refresh_all()

    def refresh_state_list(self):
        self.state_list.delete(0, tk.END)
        cell_type = self.current_cell_type()
        states = cell_type["states"] if cell_type else []
        selected = 0
        for index, state in enumerate(states):
            active = sum(1 for value in state.get("activities", {}).values() if value != 0)
            self.state_list.insert(tk.END, "{}  ({} active)".format(state["name"], active))
            if state["id"] == self.selected_state_id:
                selected = index
        if states:
            self.state_list.selection_set(selected)
            self.state_list.activate(selected)

    def refresh_state_details(self):
        state = self.current_state()
        self.state_name.delete(0, tk.END)
        self.state_phenotype.delete("1.0", tk.END)
        if not state:
            return
        self.state_name.insert(0, state.get("name", ""))
        self.state_phenotype.insert("1.0", state.get("phenotype", ""))

    def sorted_programs(self):
        cell_type = self.current_cell_type()
        state = self.current_state()
        if not cell_type or not state:
            return []
        query = self.search_var.get().strip().lower()
        programs = list(cell_type["programs"])
        if query:
            programs = [
                program for program in programs
                if query in " ".join([program["name"], program.get("category", ""), program.get("function", "")] + program.get("genes", [])).lower()
            ]
        programs.sort(
            key=lambda program: (
                -abs(state.get("activities", {}).get(program["id"], 0)),
                -state.get("activities", {}).get(program["id"], 0),
                program["name"].lower(),
            )
        )
        return programs

    def refresh_program_list(self):
        self.program_list.delete(0, tk.END)
        state = self.current_state()
        if not state:
            self.displayed_programs = []
            self.selected_program_id = None
            self.selected_program_label.config(text="No program selected")
            return
        self.displayed_programs = self.sorted_programs()
        for program in self.displayed_programs:
            level = state.get("activities", {}).get(program["id"], 0)
            label = ACTIVITY_LABELS.get(level, "baseline")
            text = "{:<12}  {:<34}  {:<24}  {}".format(label, program["name"][:34], program.get("category", "")[:24], ", ".join(program.get("genes", []))[:70])
            self.program_list.insert(tk.END, text)
        self.selected_program_id = None
        self.selected_program_label.config(text="No program selected")

    def on_state_select(self, _event):
        selection = self.state_list.curselection()
        cell_type = self.current_cell_type()
        if not selection or not cell_type:
            return
        self.selected_state_id = cell_type["states"][selection[0]]["id"]
        self.refresh_state_details()
        self.refresh_program_list()

    def on_program_select(self, _event):
        selection = self.program_list.curselection()
        if not selection:
            return
        program = self.displayed_programs[selection[0]]
        state = self.current_state()
        self.selected_program_id = program["id"]
        level = state.get("activities", {}).get(program["id"], 0)
        self.activity_var.set(ACTIVITY_LABELS.get(level, "baseline"))
        self.selected_program_label.config(text=program["name"])

    def apply_state_details(self):
        state = self.current_state()
        if not state:
            return
        name = self.state_name.get().strip()
        if not name:
            messagebox.showerror("Missing name", "State name cannot be empty.")
            return
        state["name"] = name
        state["phenotype"] = self.state_phenotype.get("1.0", tk.END).strip()
        self.mark_dirty()
        self.refresh_state_list()

    def apply_activity(self):
        if not self.selected_program_id:
            messagebox.showinfo("No program selected", "Select a program first.")
            return
        state = self.current_state()
        state.setdefault("activities", {})[self.selected_program_id] = ACTIVITY_VALUES[self.activity_var.get()]
        self.mark_dirty()
        self.refresh_state_list()
        self.refresh_program_list()

    def add_state(self):
        cell_type = self.current_cell_type()
        if not cell_type:
            return
        name = simpledialog.askstring("Add state", "State name:", parent=self)
        if not name:
            return
        state = {"id": slugify(name, {item["id"] for item in cell_type["states"]}), "name": name.strip(), "phenotype": "", "genes": [], "activities": {}}
        cell_type["states"].append(state)
        self.selected_state_id = state["id"]
        self.mark_dirty()
        self.refresh_all()

    def duplicate_state(self):
        cell_type = self.current_cell_type()
        state = self.current_state()
        if not cell_type or not state:
            return
        copied = copy.deepcopy(state)
        copied["name"] = "{} copy".format(copied["name"])
        copied["id"] = slugify(copied["name"], {item["id"] for item in cell_type["states"]})
        cell_type["states"].append(copied)
        self.selected_state_id = copied["id"]
        self.mark_dirty()
        self.refresh_all()

    def delete_state(self):
        cell_type = self.current_cell_type()
        state = self.current_state()
        if not cell_type or not state or len(cell_type["states"]) == 1:
            messagebox.showerror("Cannot delete", "The cell type needs at least one state.")
            return
        if messagebox.askyesno("Delete state", "Delete '{}'?".format(state["name"])):
            cell_type["states"] = [item for item in cell_type["states"] if item["id"] != state["id"]]
            self.selected_state_id = cell_type["states"][0]["id"]
            self.mark_dirty()
            self.refresh_all()

    def add_program(self):
        self.edit_program(None)

    def edit_selected_program(self):
        cell_type = self.current_cell_type()
        if not self.selected_program_id or not cell_type:
            messagebox.showinfo("No program selected", "Select a program first.")
            return
        program = next((item for item in cell_type["programs"] if item["id"] == self.selected_program_id), None)
        self.edit_program(program)

    def edit_program(self, program):
        if not self.current_cell_type():
            return
        ProgramEditor(self, program)

    def save_program(self, original_id, program):
        cell_type = self.current_cell_type()
        if not cell_type:
            return False
        existing = {item["id"] for item in cell_type["programs"] if item["id"] != original_id}
        if not program["id"]:
            program["id"] = slugify(program["name"], existing)
        if program["id"] in existing:
            messagebox.showerror("Duplicate id", "A program with this id already exists.")
            return False
        if original_id:
            for index, item in enumerate(cell_type["programs"]):
                if item["id"] == original_id:
                    cell_type["programs"][index] = program
                    break
        else:
            cell_type["programs"].append(program)
        self.mark_dirty()
        self.refresh_program_list()
        return True

    def _reset_selection_after_load(self):
        self.selected_cell_type_id = self.model["cellTypes"][0]["id"] if self.model["cellTypes"] else None
        cell_type = self.current_cell_type()
        self.selected_state_id = cell_type["states"][0]["id"] if cell_type and cell_type["states"] else None

    def new_from_defaults(self):
        if self.confirm_discard_changes():
            self.model = copy.deepcopy(DEFAULT_MODEL)
            self.file_path = None
            self.dirty = False
            self._reset_selection_after_load()
            self.refresh_all()

    def open_json(self):
        if not self.confirm_discard_changes():
            return
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as handle:
                self.model = validate_model(json.load(handle))
        except Exception as exc:
            messagebox.showerror("Could not open file", str(exc))
            return
        self.file_path = path
        self.dirty = False
        self._reset_selection_after_load()
        self.refresh_all()

    def save(self):
        if not self.file_path:
            return self.save_as()
        try:
            with open(self.file_path, "w", encoding="utf-8") as handle:
                json.dump(self.model, handle, indent=2)
                handle.write("\n")
        except Exception as exc:
            messagebox.showerror("Could not save file", str(exc))
            return False
        self.dirty = False
        self.update_status()
        return True

    def save_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", initialfile="islet-cell-state-model.json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if not path:
            return False
        self.file_path = path
        return self.save()

    def confirm_discard_changes(self):
        if not self.dirty:
            return True
        choice = messagebox.askyesnocancel("Unsaved changes", "Save changes before continuing?")
        if choice is None:
            return False
        return self.save() if choice else True

    def on_close(self):
        if self.confirm_discard_changes():
            self.destroy()


class ProgramEditor(tk.Toplevel):
    def __init__(self, app, program):
        tk.Toplevel.__init__(self, app)
        self.app = app
        self.original_id = program["id"] if program else None
        self.title("Edit program" if program else "Add program")
        self.geometry("560x360")
        self.transient(app)
        self.grab_set()
        data = program or {"id": "", "name": "", "category": "", "function": "", "genes": []}
        self.entries = {}
        fields = [("ID", "id"), ("Name", "name"), ("Category", "category"), ("Genes", "genes")]
        for row, (label, key) in enumerate(fields):
            tk.Label(self, text=label, anchor="w").grid(row=row, column=0, sticky="w", padx=12, pady=5)
            entry = tk.Entry(self)
            entry.grid(row=row, column=1, sticky="ew", padx=12, pady=5)
            entry.insert(0, ", ".join(data.get("genes", [])) if key == "genes" else data.get(key, ""))
            self.entries[key] = entry
        tk.Label(self, text="Function", anchor="w").grid(row=4, column=0, sticky="nw", padx=12, pady=5)
        self.function = tk.Text(self, height=5, wrap="word")
        self.function.grid(row=4, column=1, sticky="nsew", padx=12, pady=5)
        self.function.insert("1.0", data.get("function", ""))
        tk.Button(self, text="Cancel", command=self.destroy).grid(row=5, column=0, sticky="e", padx=12, pady=12)
        tk.Button(self, text="Save", command=self.save).grid(row=5, column=1, sticky="e", padx=12, pady=12)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

    def save(self):
        name = self.entries["name"].get().strip()
        if not name:
            messagebox.showerror("Missing name", "Program name cannot be empty.", parent=self)
            return
        program = {
            "id": self.entries["id"].get().strip(),
            "name": name,
            "category": self.entries["category"].get().strip(),
            "function": self.function.get("1.0", tk.END).strip(),
            "genes": split_genes(self.entries["genes"].get()),
        }
        if self.app.save_program(self.original_id, program):
            self.destroy()


if __name__ == "__main__":
    app = SimpleCellStateApp()
    app.mainloop()
