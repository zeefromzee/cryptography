# Cryptography

A collection of cryptographic algorithm implementations and attack demonstrations written in Python and C/C++. This repository is intended as an educational reference for students and practitioners who wish to study foundational concepts in classical cryptography, symmetric encryption, and stream cipher cryptanalysis.

## Table of Contents

1. [Overview](#overview)
2. [Repository Structure](#repository-structure)
3. [Components](#components)
4. [Getting Started](#getting-started)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)

## Overview

This repository covers a range of topics in both classical and modern cryptography, including:

* Implementation of the Extended Euclidean Algorithm and computation of Bezout coefficients
* A Caesar cipher implemented in C
* Symmetric file encryption using the Fernet construction from the Python `cryptography` library
* A Linear Feedback Shift Register (LFSR) implemented in C++ along with a Berlekamp-Massey attack demonstration

The code is written to be readable and instructive, prioritising clarity over performance optimisation.

## Repository Structure

```
cryptography/
    Euclidean_algorithm.py      Extended Euclidean Algorithm in Python
    ceaser_cipher.c             Caesar cipher in C
    file_encrypt.py             Fernet-based symmetric encryption in Python
    lfsr-attack/
        lsfr.cpp                LFSR implementation in C++
        berlekamp_massey.cpp    Berlekamp-Massey algorithm in C++
        attack_demo.cpp         Attack demonstration
        compare_complexity.py   Complexity comparison script
    README.md                   Project documentation
```

## Components

### Extended Euclidean Algorithm (`Euclidean_algorithm.py`)

Implements the Extended Euclidean Algorithm via a Python class. Given two integers, it computes:

* The greatest common divisor (GCD)
* The Bezout coefficients satisfying Bezout's identity
* The quotients of each input divided by the GCD

This algorithm is fundamental to modular arithmetic and underlies key generation in RSA and other public-key cryptosystems.

### Caesar Cipher (`ceaser_cipher.c`)

A C implementation of the Caesar cipher, one of the oldest and simplest substitution ciphers. The program accepts a plaintext string and a shift value from standard input and applies the shift transformation to produce ciphertext.

### Symmetric File Encryption (`file_encrypt.py`)

Demonstrates symmetric encryption and decryption using the Fernet scheme from the Python `cryptography` library. Fernet guarantees that a message encrypted with a freshly generated key cannot be read or tampered with without that key. The script accepts user input, encrypts it, and immediately demonstrates decryption to verify correctness.

### LFSR and Berlekamp-Massey Attack (`lfsr-attack/`)

Contains a C++ implementation of a Linear Feedback Shift Register (LFSR) and an implementation of the Berlekamp-Massey algorithm, which recovers the shortest LFSR that generates a given binary sequence. This directory serves as a practical demonstration of how stream ciphers based on a single LFSR are vulnerable to cryptanalytic attack given a sufficient number of output bits.

* `lsfr.cpp` -- LFSR class with configurable seed, feedback polynomial, and register length
* `berlekamp_massey.cpp` -- Berlekamp-Massey solver class
* `attack_demo.cpp` -- End-to-end demonstration of the attack
* `compare_complexity.py` -- Complexity analysis and comparison script

## Getting Started

### Prerequisites

* A C compiler (GCC or Clang) for the C source files
* A C++ compiler (G++ or Clang++) for the C++ source files
* Python 3.7 or later
* The `cryptography` Python package for `file_encrypt.py`

### Installation

Clone the repository:

```bash
git clone https://github.com/zeefromzee/cryptography.git
cd cryptography
```

Install the required Python dependency:

```bash
pip install cryptography
```

Compile the C source file:

```bash
gcc ceaser_cipher.c -o ceaser_cipher
```

Compile the C++ source files in the `lfsr-attack` directory:

```bash
g++ lfsr-attack/lsfr.cpp -o lfsr-attack/lsfr
g++ lfsr-attack/berlekamp_massey.cpp lfsr-attack/attack_demo.cpp -o lfsr-attack/attack_demo
```

## Usage

### Extended Euclidean Algorithm

```bash
python Euclidean_algorithm.py
```

The script runs with a built-in example (66528 and 52920) and prints the GCD, Bezout coefficients, and quotients to standard output. Modify the final line of the file to supply different inputs.

### Caesar Cipher

```bash
./ceaser_cipher
```

Follow the prompts to enter a plaintext string and a shift value.

### Symmetric Encryption

```bash
python file_encrypt.py
```

Enter the data to encrypt when prompted. The script prints the ciphertext and then the decrypted result.

### LFSR and Attack Demonstration

```bash
./lfsr-attack/lsfr
./lfsr-attack/attack_demo
python lfsr-attack/compare_complexity.py
```

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes with clear, descriptive messages.
4. Open a pull request describing the motivation and scope of your changes.

Please ensure that any new code includes comments explaining the algorithm or technique being demonstrated, and that existing functionality is not broken.

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software in accordance with the terms of that license.
