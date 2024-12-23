import networkx as nx

if __name__ == "__main__":
    with open("day_23/input.txt") as f:
        cons = [tuple(con.strip().split("-")) for con in f.readlines()]

    G = nx.Graph()
    [G.add_edge(*con) for con in cons]

    total = 0
    for i, cycle in enumerate(nx.chordless_cycles(G, 3)):
        if any(c[0] == "t" for c in cycle):
            total += 1
    print(f"PART 1: {total}")

    max_length = 0
    for clique in nx.find_cliques(G):
        if len(clique) > max_length:
            max_length = len(clique)
    for clique in nx.find_cliques(G):
        if len(clique) == max_length:
            break
    print(f"PART 2: {",".join(sorted(clique))}")
