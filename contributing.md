# How to Contribute

Welcome to the **LOTM-Reader** project! 🧐

First off, **thank you** for considering contributing. This project relies on fans like you to fix typos, improve formatting, and ensure the reading experience is perfect for everyone.

**Don't worry if you are not a programmer or have never used GitHub before.** This guide is written specifically for you! You cannot "break" the website, so feel free to jump in.

---

## 📚 Table of Contents

1.  [The Easy Guide: How to Edit](#-the-easy-guide-how-to-edit)
2.  [Markdown Cheat Sheet (Formatting)](#-markdown-cheat-sheet)
3.  [How to Add Footnotes](#-how-to-add-footnotes)
4.  [Adding Images](#-adding-images)
5.  [What Should I Fix?](#-what-should-i-fix)

---

## 🚀 The Easy Guide: How to Edit

You can edit chapters directly in your web browser. You don't need to download anything! you can follow these steps or directly report any issues in our community [**discord server here.**](https://discord.gg/XmzJVsyuTQ)

### Step 1: Find the Chapter
1.  Navigate to the `chapters` folder in this repository.
2.  Click on the folder for the book (e.g., `lotm` or `coi`).
3.  Click on the translation source (e.g., `webnovel`).
4.  Find the `.md` file for the chapter you want to fix (e.g., `1.md` for Chapter 1).

### Step 2: Click the Pencil
1.  Look at the top-right corner of the file viewer.
2.  Click the **Pencil Icon** (✏️) that says "Edit this file".
    * *Note: If you don't have a GitHub account, it will ask you to sign up. It's free and takes 1 minute!*
3.  GitHub will create a "Fork" (your own personal copy) of the file. This is normal!

### Step 3: Make Your Changes
1.  You are now in the **Web Editor**. It looks like a normal text box.
2.  Fix the typos, add bolding, or correct the spacing.
3.  **Preview:** Click the "Preview" tab at the top of the editor to see how your changes look before saving.

### Step 4: Save (Commit) & Submit
1.  Scroll to the bottom of the page to the **"Commit changes"** box.
2.  **Commit message:** Write a short sentence about what you did.
    * *Example:* "Fixed typo in paragraph 3" or "Added missing scene break".
3.  Click the green **"Propose changes"** button.
4.  On the next page, click the green **"Create pull request"** button.
5.  Click **"Create pull request"** one more time to confirm.

🎉 **Done!** You have submitted your changes. A maintainer will review them and merge them into the site.

---

## 📝 Markdown Cheat Sheet

This project uses **Markdown** (specifically GFM/Pandoc). It is a very simple way to style text. Here are the basics you need to know:

### 1. Italics & Bold
* To make text *italic* (for internal thoughts or emphasis), put one asterisk around it:
    * Type: `*The Fool that doesn't belong to this era...*`
    * Result: *The Fool that doesn't belong to this era...*
* To make text **bold** (for sound effects or shouting), put two asterisks around it:
    * Type: `**Bang!**`
    * Result: **Bang!**

### 2. Scene Breaks
If the scene changes or time passes, insert a horizontal line.
* Type three dashes on a new line: `---`

### 3. Headers
For chapter titles or section dividers.
* Type: `# Chapter 1` (Main Title)
* Type: `### Part 1` (Smaller Subtitle)

> 🔗 **Want to learn more?** Check out the [GitHub Markdown Guide](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) for a full tutorial.

---

## 🦶 How to Add Footnotes

Webnovels often have translation notes (T/N). Since we use Pandoc, adding footnotes is very easy!

### The Inline Method (Recommended)
You can write the note directly inside the sentence using a caret `^` and brackets `[]`.

**How to type it:**
```text
Klein looked at the potion formula^[A sequence 9 potion formula].