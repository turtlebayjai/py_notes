#!/usr/bin/env python3


def main():
    try:
        # f = open("testfile.txt", "r")
        val = name_error
    except FileNotFoundError as e:
        print(e, ": Sorry, this file does not exist!")
    except Exception as e:
        print(type(e), e.args)
        print("Sorry, something went wrong.")
    else:
        # Executes if no exception raised
        print(f.read())
        f.close()
    finally:
        # Executes regardless of exception raised
        print("Executing 'finally'...")

    # Continues if no exception / exception handled (not raised)
    print("main() execution continues...")


if __name__ == "__main__":
    main()
