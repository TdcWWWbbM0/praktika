def countjewelsinstones(J, S):
    jewels = set(J)
    count = sum(stone in jewels for stone in S)
    return count
J = "aA"
S = "aAbb"
print(count_jewels_in_stones(J, S))