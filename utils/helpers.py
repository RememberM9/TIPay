RARE_CHAR = chr(31)  # Unit Separator


# 🔒 Obfuscator
def obfuscate(text: str):
    return ''.join(chr(ord(c) + 3) for c in text[::-1])

# 🔓 Deobfuscator
def deobfuscate(obf_text: str):
    return ''.join(chr(ord(c) - 3) for c in obf_text)[::-1]

# 🧪 Example
original = "wallet_balance = 1000"
obf = obfuscate(original)
deobf = deobfuscate(obf)

print("Original:", original)
print("Obfuscated:", obf)
print("Deobfuscated:", deobf)
