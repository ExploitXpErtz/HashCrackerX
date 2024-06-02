# HashCrackerX by ExploitXpErtz

**Disclaimer:**
Any actions and/or activities related to HashCrackerX are solely your responsibility. Misuse of this tool can result in criminal charges brought against the persons in question. The contributors will not be held responsible for any criminal charges brought against individuals misusing this toolkit to break the law. This tool is made for educational purposes only. Do not attempt to violate the law with anything contained here.

## Features:
- **Automatic Hash Type Detection:** Automatically detects the hash type for well-known hash types.
- **High-Speed Performance:** Much faster than other hash cracking tools on the internet.
- **Online Wordlist Support:** Can use online Wordlists for Hash Cracking.
- **Output Support:** Save output of Cracked hashes.
- **Verbosity Control:** Adjust the level of detail in the output for better insights.
- **Custom Salt Support:** Use custom salts to crack salted hashes.

## Purpose:
HashCrackerX is designed for educational and ethical hacking purposes. It is intended to help security professionals and enthusiasts understand the process of hash cracking and enhance their knowledge in cybersecurity.

**Note:** Use this tool responsibly and only for legal and authorized activities.

## Installation:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/ExploitXpErtz/HashCrackerX.git
    cd HashCrackerX
    ```
2. **Run the tool:**
    ```bash
    python3 HashCrackerX.py
    ```

## Usage:
### Normal Hash Cracking
- python3 HashCrackerX.py hash_type hash -w /usr/share/wordlists/rockyou.txt
### Hash Cracking Using Online Wordlist
- python4 HashCrackerX.py hash_type hash -wu http://wordlist.com/file.txt
### Hash Cracking Using auto hash detection
- python4 HashCrackerX.py hash_type hash -w /usr/share/wordlists/rockyou.txt



## Contribution:
Contributions to HashCrackerX are welcome! If you have ideas for improvements or have found bugs, please open an issue or submit a pull request.

## License:
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
