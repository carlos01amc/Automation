# ⚙️ Storm Studio User Access CLI

This command-line tool allows you to quickly assign access profiles to users in Storm Studio by reading their information from a `.csv` file. 

## 🧰 Requirements

Before running this tool, make sure you have the following installed on your computer:

1. **Python 3.10+**
   - [Download Python](https://www.python.org/downloads/)
   - You can check your version by running:
     ```
     python --version
     ```

2. **Python Packages**
   Open your terminal and run this command to install the required packages:
   ```bash
   pip install requests pandas selenium
   ```
3. **Google Chrome & ChromeDriver**
   - Ensure that **Google Chrome** is installed.

## 📄 CSV Format

Your CSV must follow this format:

| Username           | Rights Profile      | Access Profile |
|--------------------|--------|------------|
| CG Agent01 (CGAgent01)  | APEU Agent Voice | AZES |
| CG Agent02 (CGAgent02)  | APEU Agent Voice | AZES |

- `username`, `rights profile`, `Acces Profile` – must match exact format in storm.

👉 **To give the user All access Profile**, leave it blank for the `Access Profile` (it will automatically select the "All Access Profile").

## 🧑‍💻 How to Use It (Step by Step)

1. **Open terminal** in the folder where the scripts are.
2. **Run the script**:
   ```
   python login.py
   ```

3. **When prompted**, type the organization name and wait for it to load, then paste the full path to your `.csv` file (e.g., `C:\Users\you\Documents\users.csv` or `./test.csv`).
4. The script will:
   - ✅ Check the file exists and has correct headers.
   - 🔍 Loop through each user row.
   - 🔐 Log into Storm Studio.
   - 📥 Assign the corresponding profile.
   - ✅ If `Access Profile is blank`, it automatically fetches to All Access Profile.

## 📌 Notes

- The script prints progress and results to the screen.

## 🙋 Need Help?

If anything doesn’t work, double-check:
- That your `.csv` file is correctly formatted.
- You’ve entered the correct path.
- Your Organization credentials are valid.

## 🚧 Planned Improvements

- **Robust Error Handling:** Improve error handling so the script doesn't exit on common issues—errors will be logged, and the script will continue processing other users.
- **Retry Logic:** Add automatic retries for failed validations or network errors to increase reliability.
- **Headless Selenium Support:** Integrate headless Selenium to allow running the script without opening a browser window.
- **Enhanced Prompts:** Make user prompts clearer and more informative for a smoother experience.