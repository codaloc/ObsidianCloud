import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def encrypt(f,k,n,origin,destination):
    fp = os.path.join(origin,f)
    aes_key = pad(k.encode(), 16)
    cipher = AES.new(aes_key, AES.MODE_CTR, nonce=n)
    with open(fp,"rb") as file:
        data = file.read()
        ciphertext = cipher.encrypt(data)
        encrypted_filename = cipher.encrypt(f.encode())

    with open(os.path.join(destination, bytes.hex(encrypted_filename)+".aes"), "wb") as file:
        file.write(cipher.nonce)
        file.write(ciphertext)


def encrypt_inset_dir(target_dir,k,n,current_dir,destination_path):
    print(f"target_dir:{target_dir}")
    print(f"current_dir:{current_dir}")
    print(f"destination_path:{destination_path}")

    aes_key = pad(k.encode(), 16)
    cipher = AES.new(aes_key, AES.MODE_CTR, nonce=n)
    encrypted_folder_name = bytes.hex(cipher.encrypt(target_dir.encode()))

    encrypted_new_destination = os.path.join(destination_path,encrypted_folder_name)
    if not os.path.exists(encrypted_new_destination):
        os.mkdir(encrypted_new_destination)
    inset_dir_path = os.path.join(current_dir,target_dir)
    encrypt_dir(inset_dir_path,k,n,encrypted_new_destination)


def decrypt(f,k,origin,destination):
    fp = os.path.join(origin,f)
    with open(fp, "rb") as file:
        nonce = file.read(8)
        ciphertext = file.read()

    aes_key = pad(k.encode(), 16)
    cipher = AES.new(aes_key, AES.MODE_CTR, nonce=nonce)
    data = cipher.decrypt(ciphertext)
    f_noext = f[:-4]
    dfn = cipher.decrypt(bytes.fromhex(f_noext)).decode()
    with open(os.path.join(destination,dfn), "wb") as file:
        file.write(data)


def decrypt_inset_dir(target_dir,k,n,current_dir,destination_path):
    print()
    print(f"target_dir:{target_dir}")
    print(f"current_dir:{current_dir}")
    print(f"destination_path:{destination_path}")
    aes_key = pad(k.encode(), 16)
    cipher = AES.new(aes_key, AES.MODE_CTR, nonce=n)
    decrypted_target_dir = cipher.decrypt(bytes.fromhex(target_dir))
    print(decrypted_target_dir)

    decrypted_new_destination = os.path.join(destination_path, decrypted_target_dir.decode())
    if not os.path.exists(decrypted_new_destination):
        os.mkdir(decrypted_target_dir)

    inset_dir_path = os.path.join(current_dir, target_dir)
    decrypt_dir(inset_dir_path, k, n, decrypted_new_destination)


def encrypt_dir(target_dir,k,n,destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    for file_name in os.listdir(target_dir):
        if not os.path.isdir(os.path.join(target_dir,file_name)):
            encrypt(file_name,k,n,target_dir,destination)
        else:
            encrypt_inset_dir(file_name,k,n,target_dir,destination)



def decrypt_dir(target_dir,k,n,destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    for file_name in os.listdir(target_dir):
        if not os.path.isdir(os.path.join(target_dir,file_name)):
            decrypt(file_name,k,target_dir,destination)
        else:
            decrypt_inset_dir(file_name,k,n,target_dir,destination)



if __name__ == "__main__":
    key = "working?"
    setnonce = b"\x00" * 8

    #origin_folder = os.path.join(os.getcwd(), "fake-sparc")
    origin_folder = "fake-sparc"
    encrypted_folder = "encrypted"
    decrypted_folder = "decrypted"

    #encrypt_inset_dirs(origin_folder,key,setnonce,encrypted_folder)
    #encrypt_dir(origin_folder,key,setnonce,encrypted_folder)
    decrypt_dir(encrypted_folder,key,setnonce,decrypted_folder)
