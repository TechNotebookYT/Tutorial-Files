import colorama

colorama.init()

print(colorama.Fore.RED + "Hello World")
print(colorama.Fore.RESET)

print(colorama.Back.RED + colorama.Fore.BLACK + "Hello World")
print(colorama.Fore.RESET)
print(colorama.Back.RESET)

print(colorama.Style.DIM + "YouTube")
print(colorama.Style.NORMAL + "YouTube")
print(colorama.Style.BRIGHT + "YouTube")

print(colorama.Back.RED + colorama.Fore.BLACK + "Hello World")

print(colorama.Style.RESET_ALL)

print("This is normal text again")
