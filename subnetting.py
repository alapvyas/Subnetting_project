from flask import Flask, render_template, request, redirect, session
import ipaddress
import random
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key for production

def generate_random_ipv4_address(subnet):
    return ipaddress.IPv4Address(random.randint(int(subnet.network_address), int(subnet.broadcast_address)))

def generate_random_cidr_prefix():
    return random.randint(8, 30)

def generate_subnetting_question():
    while True:
        random_ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        random_cidr_prefix = generate_random_cidr_prefix()
        if random_cidr_prefix > 30:
            continue
        try:
            subnet = ipaddress.IPv4Network(f'{random_ip}/{random_cidr_prefix}')
            host_addresses = [str(ip) for ip in subnet.hosts()]

            if not host_addresses:
                continue
            question_address = random.choice(host_addresses)
            return question_address, subnet
        except ValueError:
            continue

@app.route('/settings', methods=['GET', 'POST'])
def quiz_settings():
    if request.method == 'POST':
        try:
            total_questions = int(request.form['total_questions'])
        except ValueError:
            total_questions = 5

        session['question_details'] = []
        session['correct_answers'] = 0
        session['total_questions'] = total_questions
        session['current_question_number'] = 0

        return redirect('/')

    return render_template('settings.html')

@app.route('/', methods=['GET', 'POST'])
def ipv4_quiz():
    if 'question_details' not in session:
        return redirect('/settings')

    if request.method == 'POST':
        user_answer_network = request.form['network_address']
        user_answer_broadcast = request.form['broadcast_address']
        user_answer_first_host = request.form['first_usable_host']
        user_answer_last_host = request.form['last_usable_host']
        subnet = ipaddress.IPv4Network(session['current_subnet'])

        is_correct = (user_answer_network == str(subnet.network_address) and
                      user_answer_broadcast == str(subnet.broadcast_address) and
                      user_answer_first_host == str(subnet.network_address + 1) and
                      user_answer_last_host == str(subnet.broadcast_address - 1))

        session['correct_answers'] += int(is_correct)
        end_time = time.time()
        question_time = end_time - session['start_time']

        question_detail = {
            "Question Address": session['current_question_address'],
            "Subnet": session['current_subnet'],
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
        session['question_details'].append(question_detail)

        if session['current_question_number'] >= session['total_questions']:
            return redirect('/result')

    if session['current_question_number'] >= session['total_questions']:
        return redirect('/result')

    session['current_question_number'] += 1
    question_address, subnet = generate_subnetting_question()
    session['current_question_address'] = f"{str(question_address)}/{subnet.prefixlen}"
    session['current_subnet'] = str(subnet)
    session['start_time'] = time.time()

    return render_template('quiz.html', 
                           current_question_number=session['current_question_number'],
                           total_questions=session['total_questions'],
                           current_question_address=session['current_question_address'])

@app.route('/result')
def quiz_result():
    question_details = session.get('question_details', [])
    correct_answers = session.get('correct_answers', 0)
    total_questions = session.get('total_questions', 0)
    total_time = sum(detail['Time Taken (seconds)'] for detail in question_details)
    average_time = total_time / total_questions if total_questions > 0 else 0

    session.clear()

    return render_template('result.html',
                           correct_answers=correct_answers,
                           total_questions=total_questions,
                           question_details=question_details,
                           average_time=average_time)

@app.route('/home')
def home():
    return redirect('/settings')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
