# -*- coding:utf-8 -*-

"""
@author: delu
@file: rsa_utils.py
@time: 17/6/1 14:48
"""
from Crypto.Hash import SHA
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
import base64


class RsaUtils(object):
    @staticmethod
    def sign(content, private_key):
        """
        生成签名
        :param content: 
        :param private_key: 
        :return: 
        """
        private_key_list = ['-----BEGIN RSA PRIVATE KEY-----']
        while True:
            private_key_list.append(private_key[0:64])
            private_key = private_key.replace(private_key[0:64], '')
            if len(private_key) <= 0:
                break
        private_key_list.append('-----END RSA PRIVATE KEY-----')
        private_key = '\n'.join(private_key_list)
        rsakey = RSA.importKey(private_key)
        signer = Signature_pkcs1_v1_5.new(rsakey)
        digest = SHA.new()
        digest.update(content)
        sign = signer.sign(digest)
        return base64.b64encode(sign)

    @staticmethod
    def verify(signature, content, public_key):
        """
        验签
        :param signature: 
        :param content: 
        :param public_key: 
        :return: 
        """
        public_key_list = ['-----BEGIN PUBLIC KEY-----']
        while True:
            public_key_list.append(public_key[0:64])
            public_key = public_key.replace(public_key[0:64], '')
            if len(public_key) <= 0:
                break
        public_key_list.append('-----END PUBLIC KEY-----')
        public_key = '\n'.join(public_key_list)
        rsakey = RSA.importKey(public_key)
        verifier = Signature_pkcs1_v1_5.new(rsakey)
        digest = SHA.new()
        digest.update(content)
        is_verify = verifier.verify(digest, base64.b64decode(signature))
        return is_verify


if __name__ == '__main__':
    #  签名
    content = 'buyer_id=1&hello=2'
    private_key = 'MIICXAIBAAKBgQCpPZXSUCyJAUJIXvxYpsHZNLzcYEK+f/U6wrSd36KofYTA0Z8l' \
                  'kEgPR4bYOCEXKd7v45pyM8A1pMqjCdJnveipswMH6EvUVI2bE2CJmfa/NXzeccKG' \
                  'p1vKfSqsse4JSY5RlNk0JWpi0sBKFP0wwYevdb6oF230lEiRM7SgStQwawIDAQAB' \
                  'AoGARNva3pRiWmgZuOp0z/khfCe6BAxie7ICbCMWa/m268kOP4nKr/TxbM4UblsA' \
                  'E7WkkIRRrc+ij/D5xbZUVoNtax0S/K6ENP4oawM3dOkPrvZ+g/fwruPTnyFySiOM' \
                  '2gmmm2FunKdlJBjWyeY0LjCqfOyATrlKt99ArfOXa3G+HnECQQDUA9Uhmpp7l8rL' \
                  'Lo91TVTJakf7/Y640Qw1c4kH4qDkx8bLWJjho3XaxasKX3Xaz0hsJH5NJ8WODEDu' \
                  'scDkshh5AkEAzFn+Wh7DkIn36rM4HDA3rmh9TVXEMHRsG6KPQnuki9MZc6AE0sLB' \
                  'GBgWh9YDvhMQnO5IEwN/EJlU8UVu6rFfAwJAYNgfUuo8BpifmY/7F6nrQNW7a++2' \
                  'cdWLrh7ISUHMHLTkqZ4et3LjMrt4FZTlUL2+ZyeESdoQ84HFZ0LqyYxQgQJBAJoP' \
                  'PrKyfr15Rm6qrqKRt2jFXbHv9viQzPAInfiBPowrmgSRnxFFwk1n25SMxEWIGf41' \
                  'piCvghwBfQhoUDafggECQGVq5KaQVefPZPQ0SgMFBrOjqBrJOIhnHOGkoeR9MjZY' \
                  'kwwaLUBLwJF5w0BfM9o2WN7o0esWbFZ99CtHkmHUCMo='
    sign = RsaUtils.sign(content, private_key)
    print sign

    public_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCpPZXSUCyJAUJIXvxYpsHZNLzc' \
                 'YEK+f/U6wrSd36KofYTA0Z8lkEgPR4bYOCEXKd7v45pyM8A1pMqjCdJnveipswMH' \
                 '6EvUVI2bE2CJmfa/NXzeccKGp1vKfSqsse4JSY5RlNk0JWpi0sBKFP0wwYevdb6o' \
                 'F230lEiRM7SgStQwawIDAQAB'
    print RsaUtils.verify(sign, content, public_key)
