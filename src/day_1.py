input = open('../inputs/day_1.txt', 'r')
lines = input.readlines()

elf_packs = []
current = 0
for line in lines:
    if line != '\n':
        current = current + int(line)
    else:
        elf_packs.append(current)
        current = 0

print(sorted(elf_packs, reverse=True)[0])
print(sum(sorted(elf_packs, reverse=True)[0:3]))