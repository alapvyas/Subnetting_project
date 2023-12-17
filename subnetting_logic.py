import ipaddress
import random
import time

def generate_random_ipv4_address(subnet):
    return ipaddress.IPv4Address(random.randint(int(subnet.network_address), int(subnet.broadcast_address)))

def generate_random_cidr_prefix():
    return random.randint(8, 30)

def generate_subnetting_question():
    while True:
        random_ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        random_cidr_prefix = generate_random_cidr_prefix()
        try:
            subnet = ipaddress.IPv4Network(f'{random_ip}/{random_cidr_prefix}')
            question_address = generate_random_ipv4_address(subnet)
            return question_address, subnet
        except ValueError:
            continue

def ipv4():
    correct_answers = 0
    total_questions = 5
    total_time = 0

    question_dict = {}  # Dictionary to store question details

    for i in range(total_questions):
        question_address, subnet = generate_subnetting_question()
        print(f"What is the network address of {question_address}/{subnet.prefixlen}?")
        start_time = time.time()

        user_answer_network = input("Your answer (Network Address): ")
        user_answer_broadcast = input("Your answer (Broadcast Address): ")
        user_answer_first_host = input("Your answer (First Usable Host): ")
        user_answer_last_host = input("Your answer (Last Usable Host): ")

        end_time = time.time()
        question_time = end_time - start_time
        total_time += question_time

        is_correct = (user_answer_network == str(subnet.network_address) and
                      user_answer_broadcast == str(subnet.broadcast_address) and
                      user_answer_first_host == str(subnet.network_address + 1) and
                      user_answer_last_host == str(subnet.broadcast_address - 1))

        if is_correct:
            print("Correct!")
            correct_answers += 1
        else:
            print(f"Sorry, the correct answers were:")
            print(f"Network Address: {subnet.network_address}")
            print(f"Broadcast Address: {subnet.broadcast_address}")
            print(f"First Usable Host: {subnet.network_address + 1}")
            print(f"Last Usable Host: {subnet.broadcast_address - 1}")

        print(f"Time taken: {question_time:.2f} seconds")
        print("Press Enter for the next question.")
        input()

        # Storing the question and answers in the dictionary
        question_dict[i + 1] = {
            "Question Address": str(question_address),
            "Subnet": str(subnet),
            "User Answers": {
                "Network Address": user_answer_network,
                "Broadcast Address": user_answer_broadcast,
                "First Usable Host": user_answer_first_host,
                "Last Usable Host": user_answer_last_host
            },
            "Correct Answers": {
                "Network Address": str(subnet.network_address),
                "Broadcast Address": str(subnet.broadcast_address),
                "First Usable Host": str(subnet.network_address + 1),
                "Last Usable Host": str(subnet.broadcast_address - 1)
            },
            "Time Taken (seconds)": question_time,
            "Correct": is_correct
        }

    average_time_per_question = total_time / total_questions

    print(f"\nYou answered {correct_answers} out of {total_questions} questions correctly.")
    print(f"Average time per question: {average_time_per_question:.2f} seconds")

    return question_dict

# To use the function and get the dictionary
questions_dict = ipv4()
print(questions_dict)
