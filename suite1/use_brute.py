from brute import Brute

print("=== Brute Force password crack Demo ===")
secret = input("Enter a password consisting of 1-8 alphanumeric characters only: ")

brute = Brute(secret)
print("\nCracking your password... (this may take a while)")
print("Hash target: " + brute.target+ "\n")

# Try to crack it 10,000,000 times - this should take about 30 seconds
result = brute.bruteMany(limit=10000000)

if result == -1:
    print("Failed to crack the password within the attempt limit.")
else:
    print("Password cracked in " + str(result) + " seconds!")

