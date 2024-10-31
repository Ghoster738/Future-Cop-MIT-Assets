import MaterialTests
import Pumpkin
import Stars

if __name__ == "__main__":
    no_test_failure = True

    no_test_failure &= MaterialTests.test()
    no_test_failure &= Pumpkin.test()
    no_test_failure &= Stars.test()

    if not no_test_failure:
        print("Test failure has been found!")
