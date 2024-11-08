# Simple Electronic QSL (SEQSL)

**SEQSL** is a tool designed for amateur radio operators that automates the sending of electronic QSL cards using email.

## Features

- **Automated Sending**: Streamlines and optimizes the process of sending electronic QSL cards.
- **Automatic QRZ lookup**: Get the email automatically from QRZ.
- **GMAIL Integration**: Uses GMAIL as the email service to send QSL cards. Compatibility with other SMTP services is planned for future updates.

## Requirements

- **Python 3.6+**
- **PIP package manager**
- **GMAIL Account** with access enabled for less secure apps, or use two-factor authentication with app passwords.
- **QRZ Account** to look up the recipient's email address. A premium account is recommended to avoid lookup limits.
- **QSL file** in `.jpg` format with your QSL card. SEQSL will add a table with QSO details at the bottom of the card, so keep this area clear.
- **ADI file** containing the QSOs for which you wish to send QSL cards.

## Installation and Execution from Repository

1. Clone the repository:

   ```bash
   git clone https://github.com/dacacioa/seqsl.git
   ```
   
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Copy `config.ini.example` to `config.ini` and update it with your specific information.

## Sending QSL Cards

To send a QSL card, run the following command:

   ```bash
   python seqsl.py qslcard.jpg adifile.adi
   ```