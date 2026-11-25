import sys
from pathlib import Path

PREDEFINED_SYMBOLS = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4,
    "R5": 5, "R6": 6, "R7": 7, "R8": 8, "R9": 9,
    "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15,
    "SCREEN": 16384, "KBD": 24576,
}

COMP_TABLE = {
    "0":   "0101010", "1":   "0111111", "-1":  "0111010",
    "D":   "0001100", "A":   "0110000", "M":   "1110000",
    "!D":  "0001101", "!A":  "0110001", "!M":  "1110001",
    "-D":  "0001111", "-A":  "0110011", "-M":  "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "A+D": "0000010", "D+M": "1000010", "M+D": "1000010", "D-A": "0010011",
    "D-M": "1010011", "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "A&D": "0000000", "D&M": "1000000", "M&D": "1000000",
    "D|A": "0010101", "A|D": "0010101", "D|M": "1010101", "M|D": "1010101",
}

DEST_TABLE = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111",
}

JUMP_TABLE = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}


def clean_lines(raw_lines: list[str]) -> list[str]:
    cleaned = []
    for line in raw_lines:
        code = line.split("//", 1)[0].strip()
        if code:
            cleaned.append(code)
    return cleaned


def encode_c_instruction(inst: str) -> str:
    if "=" in inst:
        dest_part, rest = inst.split("=", 1)
    else:
        dest_part, rest = "", inst

    if ";" in rest:
        comp_part, jump_part = rest.split(";", 1)
    else:
        comp_part, jump_part = rest, ""

    comp_bits = COMP_TABLE[comp_part.strip()]
    dest_bits = DEST_TABLE[dest_part.strip()]
    jump_bits = JUMP_TABLE[jump_part.strip()]
    return f"111{comp_bits}{dest_bits}{jump_bits}"


def assemble(asm_path: Path) -> tuple[list[str], dict[str, int]]:
    symbols = dict(PREDEFINED_SYMBOLS)
    raw_lines = asm_path.read_text(encoding="utf-8").splitlines()
    lines = clean_lines(raw_lines)

    # First pass: record labels and instruction addresses
    instructions: list[str] = []
    rom_address = 0
    for line in lines:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1].strip()
            if label not in symbols:
                symbols[label] = rom_address
        else:
            instructions.append(line)
            rom_address += 1

    # Second pass: translate instructions & allocate variables from RAM 16
    next_var_addr = 16
    binary_lines: list[str] = []

    for inst in instructions:
        if inst.startswith("@"):
            operand = inst[1:].strip()
            if operand.isdigit():
                addr = int(operand)
            else:
                if operand not in symbols:
                    symbols[operand] = next_var_addr
                    next_var_addr += 1
                addr = symbols[operand]
            binary_lines.append(f"{addr:016b}")
        else:
            binary_lines.append(encode_c_instruction(inst))

    return binary_lines, symbols


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <program.asm>")
        sys.exit(1)

    asm_path = Path(sys.argv[1])
    binary_lines, symbols = assemble(asm_path)

    out_hack = asm_path.with_suffix(".hack")
    out_hack.write_text("\n".join(binary_lines) + "\n", encoding="utf-8")

    # Additional Feature for K = 75 (K mod 3 == 0):
    # Save all labels and variables with their addresses in symbols.txt
    out_symbols = asm_path.parent / "symbols.txt"
    symbol_entries = [f"{name}: {addr}" for name, addr in symbols.items()]
    out_symbols.write_text("\n".join(symbol_entries) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
