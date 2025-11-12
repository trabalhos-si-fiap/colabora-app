import hashlib
import os
import hmac

from src.models.users import User


PasswordHash = bytes
Salt = bytes

class PasswordManager:
    # Fatores de custo n r p
    n=16384
    r=8
    p=1
    dklen=64 # Tamanho da chave derivada (hash)

    def _gen_salt(self):
        return os.urandom(16)
    
    def hash_password(self, password: str) -> tuple[PasswordHash, Salt]:
        """
        Função para criar o hash da senha do usuário.
        Retornar uma tupla com o hash e o salt.
        """
        salt = self._gen_salt()
        hash_password = hashlib.scrypt(
            password.encode(), 
            salt=salt, 
            n=self.n, 
            r=self.r, 
            p=self.p,
            dklen=self.dklen
        )

        return hash_password, salt
    

    def check_password(self, password: str, user: User) -> bool:
        """                
        Função para verificar se a senha está correta.
        Retorna True se a senha estiver correta, False caso contrário.
        """
        user_salt = user.salt

        hash_teste = hashlib.scrypt(
            password.encode(), 
            salt=user_salt, 
            n=self.n, 
            r=self.r, 
            p=self.p,
            dklen=self.dklen
        )
        if hmac.compare_digest(user.password, hash_teste):
            print("Login bem-sucedido!")
            return True
        print("Senha incorreta.")
        return False