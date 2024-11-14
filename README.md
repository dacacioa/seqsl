# Simple Electronic QSL (SEQSL)

**SEQSL** is a tool designed for amateur radio operators that automates the sending of electronic QSL cards using email.

## Features

- **Automated Sending**: Streamlines and optimizes the process of sending electronic QSL cards.
- **Automatic QRZ lookup**: Get the email automatically from QRZ.
- **SMTP Integration**: Uses Gmail or another SMTP server to send emails.

## Requirements
 
- **Python 3.6+**
- **PIP package manager**
- **SMTP Account** to send emails. If you use GMAIL you'll need enabled access for less secure apps.
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

4. Sending QSL Cards

To send a QSL card, run the following command:

   ```bash
   python seqsl.py qslcard.jpg adifile.adi
   ```

## Installation and Execution from Windows binary

1. Go to releases [https://github.com/dacacioa/seqsl/releases]

2. Copy file seqsl.exe to a local folder.

3. Download `config.ini.example` to local folder as `config.ini` and update it with your specific information. 

4. Sending QSL Cards

To send a QSL card, run the following command:

   ```cmd
   seqsl.exe qslcard.jpg adifile.adi

