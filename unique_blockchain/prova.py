import nacl.encoding
import nacl.signing

private_key = nacl.signing.SigningKey.generate()
public_key = private_key.verify_key



public_key_hex = public_key.encode(encoder=nacl.encoding.HexEncoder)


signed = private_key.sign(b"address1")



public_key = nacl.signing.VerifyKey(public_key_hex,
                                    encoder=nacl.encoding.HexEncoder)

print(public_key.verify(signed.message, signed.signature))

try:
    signed2 = public_key.verify(signed)
    print('v')
except:
    print('ciao')
verify_key = public_key.verify_key
verify_key_hex = verify_key.encode(encoder=nacl.encoding.HexEncoder)


verify_key = nacl.signing.VerifyKey(verify_key_hex,
                                    encoder=nacl.encoding.HexEncoder)
print(verify_key.verify(signed2.message, signed2.signature))