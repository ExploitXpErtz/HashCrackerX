#!/bin/python3
import hashlib
import sys
from urllib.request import urlopen
import os
import threading
from queue import Queue
from tqdm import tqdm

class HashCracker:
    def __init__(self, hash_type, hash_to_crack, wordlist, custom_hash=None, verbose=False, silent=False, salt=None, output_file=None, exit_on_found=False):
        self.hash_type = hash_type
        self.hash_to_crack = hash_to_crack
        self.wordlist = wordlist
        self.custom_hash = custom_hash
        self.verbose = verbose
        self.silent = silent
        self.salt = salt
        self.output_file = output_file
        self.exit_on_found = exit_on_found
        self.found = threading.Event()
        self.queue = Queue()

    def hash_word(self, word):
        try:
            if self.custom_hash:
                return self.custom_hash(word)
            if self.hash_type == 'MD5':
                return hashlib.md5(word.encode()).hexdigest()
            elif self.hash_type == 'SHA1':
                return hashlib.sha1(word.encode()).hexdigest()
            elif self.hash_type == 'SHA224':
                return hashlib.sha224(word.encode()).hexdigest()
            elif self.hash_type == 'SHA256':
                return hashlib.sha256(word.encode()).hexdigest()
            elif self.hash_type == 'SHA384':
                return hashlib.sha384(word.encode()).hexdigest()
            elif self.hash_type == 'SHA512':
                return hashlib.sha512(word.encode()).hexdigest()
            elif self.hash_type == 'SHA3-224':
                return hashlib.sha3_224(word.encode()).hexdigest()
            elif self.hash_type == 'SHA3-256':
                return hashlib.sha3_256(word.encode()).hexdigest()
            elif self.hash_type == 'SHA3-384':
                return hashlib.sha3_384(word.encode()).hexdigest()
            elif self.hash_type == 'SHA3-512':
                return hashlib.sha3_512(word.encode()).hexdigest()
            elif self.hash_type == 'RIPEMD160':
                return hashlib.new('ripemd160', word.encode()).hexdigest()
            elif self.hash_type == 'Whirlpool':
                return hashlib.new('whirlpool', word.encode()).hexdigest()
            elif self.hash_type == 'BLAKE2b':
                return hashlib.blake2b(word.encode()).hexdigest()
            elif self.hash_type == 'BLAKE2s':
                return hashlib.blake2s(word.encode()).hexdigest()
            else:
                print(f"Hash type {self.hash_type} is not supported.")
                return None
        except Exception as e:
            print(f"Error in hash_word: {e}")
            return None

    def load_wordlist(self):
        try:
            if self.wordlist.startswith('http://') or self.wordlist.startswith('https://'):
                response = urlopen(self.wordlist)
                return [line.decode('utf-8').strip() for line in response]
            else:
                with open(self.wordlist, 'r', errors='ignore') as file:
                    return [line.strip() for line in file if not self.found.is_set()]
        except Exception as e:
            print(f"Error loading wordlist: {e}")
            return []

    def worker(self):
        while not self.queue.empty() and not self.found.is_set():
            word = self.queue.get()
            if self.salt:
                word = self.salt + word
            hashed_word = self.hash_word(word)
            if self.verbose and not self.silent:
                print(f"Trying {word}: {hashed_word}")
            if hashed_word == self.hash_to_crack:
                self.found.set()
                if not self.silent:
                    print(f"Password found: {word}")
                if self.output_file:
                    try:
                        with open(self.output_file, 'a') as result_file:
                            result_file.write(f"{self.hash_to_crack}:{word}\n")
                    except Exception as e:
                        print(f"Error writing to output file: {e}")
                break
            self.queue.task_done()

    def crack(self, num_threads=50):
        words = self.load_wordlist()
        if not words:
            return
        if not self.silent:
            print(f"Total words to try: {len(words)}")

        for word in words:
            self.queue.put(word)

        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=self.worker)
            thread.start()
            threads.append(thread)

        with tqdm(total=len(words), disable=self.silent) as pbar:
            while not self.queue.empty() and not self.found.is_set():
                pbar.update(1)
        
        for thread in threads:
            thread.join()

def detect_hash_type(hash_value):
    try:
        hash_lengths = {
            32: 'MD5',
            40: 'SHA1',
            56: 'SHA224',
            64: 'SHA256',
            96: 'SHA384',
            128: 'SHA512',
        }
        return hash_lengths.get(len(hash_value), None)
    except Exception as e:
        print(f"Error in detect_hash_type: {e}")
        return None

if __name__ == "__main__":
    def display_logo():
        logo = """
        *************************************************
        *                                               *
        *               HashCrackerX                    *
        *                                               *
        *************************************************
        \t\t\tFollow ExploitXpErtz
        """
        print(logo)
    display_logo()
    import argparse

    parser = argparse.ArgumentParser(description='Multi-hash cracker')
    parser.add_argument('-x', '--exit', action='store_true', help='Exit the script as soon as hash is found')
    parser.add_argument('-w', '--wordlist', help='Path to the wordlist file')
    parser.add_argument('-wu', '--wordlist-url', help='URL of the raw text wordlist')
    parser.add_argument('-o', '--output', help='Output file to save cracked passwords')
    parser.add_argument('-s', '--silent', action='store_true', help='Silent mode, no output except for results')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode, detailed output')
    parser.add_argument('--salt', help='Salt to use with hash')
    parser.add_argument('hash_type', help='Hash type (auto for auto-detection)')
    parser.add_argument('hash_to_crack', help='Hash value to crack')

    args = parser.parse_args()

    if args.wordlist_url:
        wordlist_path = args.wordlist_url
    else:
        wordlist_path = args.wordlist

    hash_type = args.hash_type.upper()
    hash_to_crack = args.hash_to_crack
    custom_hash = None
    verbose = args.verbose
    silent = args.silent
    salt = args.salt
    output_file = args.output
    exit_on_found = args.exit

    if hash_type == 'AUTO':
        detected_type = detect_hash_type(hash_to_crack)
        if detected_type:
            if not silent:
                print(f"Detected hash type: {detected_type}")
            hash_cracker = HashCracker(detected_type, hash_to_crack, wordlist_path, verbose=verbose, custom_hash=custom_hash, silent=silent, salt=salt, output_file=output_file, exit_on_found=exit_on_found)
            hash_cracker.crack()
        else:
            if not silent:
                print("Unable to detect hash type. Please specify the hash type explicitly.")
    else:
        hash_cracker = HashCracker(hash_type, hash_to_crack, wordlist_path, verbose=verbose, custom_hash=custom_hash, silent=silent, salt=salt, output_file=output_file, exit_on_found=exit_on_found)
        hash_cracker.crack()

