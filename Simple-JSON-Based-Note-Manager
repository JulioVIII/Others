import os
import json
import uuid
from datetime import datetime
from shutil import copy2

NOTES_FILE = "notes.json"
BACKUP_DIR = "backups"

def ensure_storage():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def load_notes():
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_notes(notes):
    # backup current file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"notes_{timestamp}.bak.json")
    copy2(NOTES_FILE, backup_path)
    # save new
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

def multline_input(prompt="Type your content (type 'END' on a line alone to finish):"):
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
        except KeyboardInterrupt:
            print("\nInterrupted. No lines were added.")
            return None
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines)

def list_notes(notes):
    if not notes:
        print("No notes found.")
        return
    print("\n--- Notes List ---")
    for note in notes:
        ts = note.get("timestamp", "")
        title = note.get("title", "")
        nid = note.get("id")
        print(f"{nid} | {ts} | {title}")
    print("--- End of List ---\n")

def view_note(notes):
    nid = input("Enter the ID of the note to view: ").strip()
    note = next((n for n in notes if n["id"] == nid), None)
    if not note:
        print("Note not found.")
        return
    print(f"\n--- Note {nid} ---")
    print(f"Date: {note['timestamp']}")
    print(f"Title: {note['title']}")
    print("--- Content ---")
    print(note["content"])
    print("--- End of Note ---\n")

def add_note(notes):
    title = input("Note title: ").strip()
    content = multline_input("Type the content. Type 'END' to finish:")
    if content is None:
        return
    note = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": datetime.now().isoformat(sep=" ", timespec="seconds"),
        "title": title,
        "content": content
    }
    notes.append(note)
    save_notes(notes)
    print(f"Note added with ID {note['id']}.")

def append_to_note(notes):
    nid = input("ID of the note to append to: ").strip()
    note = next((n for n in notes if n["id"] == nid), None)
    if not note:
        print("Note not found.")
        return
    addition = multline_input("Type the text to append. Type 'END' to finish:")
    if addition is None:
        return
    # ensure newline separation
    if note["content"] and not note["content"].endswith("\n"):
        note["content"] += "\n"
    note["content"] += addition
    note["timestamp"] = datetime.now().isoformat(sep=" ", timespec="seconds")
    save_notes(notes)
    print("Content appended successfully.")

def overwrite_note(notes):
    nid = input("ID of the note to overwrite: ").strip()
    idx = next((i for i,n in enumerate(notes) if n["id"] == nid), None)
    if idx is None:
        print("Note not found.")
        return
    print("This will overwrite the note. A backup is automatically created.")
    new_title = input("New title (leave empty to keep current): ").strip()
    new_content = multline_input("Type the new content. Type 'END' to finish:")
    if new_content is None:
        return
    if new_title:
        notes[idx]["title"] = new_title
    notes[idx]["content"] = new_content
    notes[idx]["timestamp"] = datetime.now().isoformat(sep=" ", timespec="seconds")
    save_notes(notes)
    print("Note overwritten successfully.")

def delete_note(notes):
    nid = input("ID of the note to delete: ").strip()
    note = next((n for n in notes if n["id"] == nid), None)
    if not note:
        print("Note not found.")
        return
    confirm = input(f"Are you sure you want to delete the note '{note['title']}'? (yes/no): ").strip().lower()
    if confirm in ("yes","y"):
        notes[:] = [n for n in notes if n["id"] != nid]
        save_notes(notes)
        print("Note deleted.")
    else:
        print("Operation canceled.")

def search_notes(notes):
    q = input("Type text to search (in title or content): ").strip().lower()
    results = [n for n in notes if q in n.get("title","").lower() or q in n.get("content","").lower()]
    if not results:
        print("No matches found.")
        return
    print(f"\nFound {len(results)} match(es):")
    for n in results:
        print(f"{n['id']} | {n['timestamp']} | {n['title']}")
    print()

def export_note_txt(notes):
    nid = input("ID of the note to export as .txt: ").strip()
    note = next((n for n in notes if n["id"] == nid), None)
    if not note:
        print("Note not found.")
        return
    filename = f"note_{nid}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{note['title']}\n")
        f.write(f"{note['timestamp']}\n\n")
        f.write(note['content'])
    print(f"Note exported as {filename}")

def main_menu():
    ensure_storage()
    while True:
        notes = load_notes()
        print("\n--- NOTE MANAGER ---")
        print("1. List notes")
        print("2. View note")
        print("3. Add note")
        print("4. Append to note")
        print("5. Overwrite note")
        print("6. Search notes")
        print("7. Delete note")
        print("8. Export note to .txt")
        print("9. Exit")
        option = input("Choose an option (1-9): ").strip()
        if option == "1":
            list_notes(notes)
        elif option == "2":
            view_note(notes)
        elif option == "3":
            add_note(notes)
        elif option == "4":
            append_to_note(notes)
        elif option == "5":
            overwrite_note(notes)
        elif option == "6":
            search_notes(notes)
        elif option == "7":
            delete_note(notes)
        elif option == "8":
            export_note_txt(notes)
        elif option == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main_menu()
