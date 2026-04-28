import simplecli as cli

def add(nums: list[int]):
    print(sum(nums))

cli.add("add", add, {"nums": list[int]})

cli.run()