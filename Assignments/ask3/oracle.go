package main

import (
	"crypto/rand"
	"crypto/rsa"
	"log"
	"math/big"
	"net"
	"net/rpc"
)

type Oracle struct {
	PrivateKey *rsa.PrivateKey
}

type PublicKeyReply struct {
	PublicKey rsa.PublicKey
}

type MyBigInt = *big.Int

type LocArgs struct {
	Cipher MyBigInt
}

type LocReply struct {
	IsInFirstHalf bool
}

// Function that computes base ** exponent (mod modulus)
func modPower(base, exponent, modulus *big.Int) *big.Int {

	result := big.NewInt(1)
	exp := new(big.Int).Set(exponent)

	// Repeated squaring
	for exp.BitLen() > 0 {
		if exp.Bit(0) == 1 {
			result = result.Mul(result, base)
			result = result.Mod(result, modulus)
		}
		exp = exp.Rsh(exp, 1)
		base = base.Mul(base, base)
		base = base.Mod(base, modulus)
	}

	return result

}

// Function that sends the public key for RSA encryption to client
func (o *Oracle) GetPublicKey(args struct{}, reply *PublicKeyReply) error {
	reply.PublicKey = o.PrivateKey.PublicKey
	return nil
}

// Function that gets a ciphertext, decrypts it
// and sends true if the decryption is in the first
// half of [0, N-1] and false otherwise
func (o *Oracle) Loc(args *LocArgs, reply *LocReply) error {
	var a *big.Int
	var b *big.Int

	// Decrypt the cipher using private key
	a = modPower(args.Cipher, o.PrivateKey.D, o.PrivateKey.PublicKey.N)
	// Compute the middle of the space of valid values
	b = new(big.Int).Div(o.PrivateKey.PublicKey.N, big.NewInt(2))

	if a.Cmp(b) < 0 {
		reply.IsInFirstHalf = true
	} else {
		reply.IsInFirstHalf = false
	}

	return nil
}

func main() {
	// Generate RSA key pair
	privateKey, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		log.Fatal("Error generating RSA key pair:", err)
	}

	// Create the listener (Oracle)
	oracle := &Oracle{
		PrivateKey: privateKey}

	rpc.Register(oracle)

	listener, err := net.Listen("tcp", ":1234")
	if err != nil {
		log.Fatal("Error starting listener:", err)
	}
	defer listener.Close()

	log.Println("Listening for RPC connections on port 1234...")
	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Fatal("Error accepting connection:", err)
		}
		go rpc.ServeConn(conn)
	}
}
