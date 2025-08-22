# iD01t Academy - Python Exercises Book 2 · Edition #2

🚀 **Premium 2025 Dark Suite** — A single-file Python desktop application bundling **12 full-featured mini-apps** with a modern GUI.  
This project is built to accompany **Python Exercises Book 2 · Edition #2**, bringing every exercise to life as a real application.

---

## ✨ Features

- **All-in-One Application**: 12 polished tools combined in a single `.py` file
- **Modern Dark UI (2025 style)** with [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap)  
- **Auto Dependency Installation** on first run  
- **Persistent Storage** (JSON per module in `./data/`)  
- **Data Export**: Save everything as a ZIP in one click  
- **Cross-Platform**: Runs on Windows, macOS, Linux  
- **Packaged Ready** for Microsoft Store, PyInstaller, or standalone release  

### Included Apps
1. 💰 Expense Tracker (with CSV export & charts)  
2. 🏞️ Mini Adventure Game (branching text story)  
3. 🔐 Password Vault (demo encryption, educational only)  
4. ✅ To-Do List Manager  
5. 🌐 Web Scraper (titles + first 20 links)  
6. 📏 Unit Converter (length, weight, temperature)  
7. 🎯 Quiz Game (Python basics)  
8. ☁️ Weather (Open-Meteo, no API key required)  
9. 📊 Plotter (comma-separated values graph)  
10. 🗓️ Reminders (dated notes, persistent)  
11. 📝 Text Tools (word count & frequency)  
12. ⏱️ Timer (countdown with live updates)  

Each tab includes a **"View Tab Code"** button so learners can explore the source.

---

## 🛠️ Installation

### Requirements
- Python **3.9+**
- Windows, macOS, or Linux

### Clone and Run
```bash
git clone https://github.com/your-username/id01t-academy-exercises-book2.git
cd id01t-academy-exercises-book2
python main.py
````

On first run, dependencies are automatically installed:

* `ttkbootstrap`
* `requests`
* `beautifulsoup4`
* `matplotlib`
* `pillow`

---

## 📦 Build Executable (Windows)

Use [PyInstaller](https://pyinstaller.org/):

```bash
pyinstaller --noconfirm --windowed --icon icon.ico main.py
```

This will generate a `.exe` file you can distribute or publish to the Microsoft Store.

---

## 📁 Project Structure

```
├── main.py                # The all-in-one script (this repo’s core)
├── icon.ico               # Application icon (place in root)
├── data/                  # Local storage for each app
├── README.md              # This file
```

---

## 🎨 Screenshots

*(Add your screenshots here for GitHub preview)*

---

## 📚 About

This project was created by **Guillaume Lessard** under **iD01t Productions**
to demonstrate how learning exercises can evolve into **real, production-grade applications**.

🌐 Website: [id01t.store](https://id01t.store)
📧 Contact: [admin@id01t.store](mailto:admin@id01t.store)

---

## ⚠️ Disclaimer

This application is for **educational purposes only**.
Do not use the Password Vault for sensitive or real credentials. Always use a trusted password manager in production.

---

## ⭐ Contributing

Contributions are welcome!
Fork, improve the apps, or add your own tab, then submit a Pull Request.

---

## 📜 License

Released under the **MIT License**.
You are free to use, modify, and distribute with attribution.

```

