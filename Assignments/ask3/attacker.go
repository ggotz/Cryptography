package main

import (
	"crypto/rsa"
	"fmt"
	"log"
	"math/big"
	"net/rpc"
)

type OracleClient struct {
	client *rpc.Client
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

// Function that makes an RPC call to Oracle to get the Public Key
func (o *OracleClient) GetPublicKey() (PublicKeyReply, error) {
	var reply PublicKeyReply
	err := o.client.Call("Oracle.GetPublicKey", struct{}{}, &reply)
	if err != nil {
		return PublicKeyReply{}, err
	}
	return reply, nil
}

// Function that makes an RPC call to Oracle for a specific cipher and gets the value of loc function
func (o *OracleClient) Loc(args LocArgs, reply *LocReply) error {
	err := o.client.Call("Oracle.Loc", args, reply)
	return err
}

// Function that computes 2 to the power of exponent (mod modulus)
func modPowerofTwo(exponent int, modulus *big.Int) *big.Int {
	var res *big.Int
	var tmp *big.Int

	res = big.NewInt(1)

	for exponent > 0 {
		tmp = new(big.Int).Mul(big.NewInt(2), res)
		res = new(big.Int).Mod(tmp, modulus)
		exponent--
	}
	return res
}

// Function that computes base**exponent (mod modulus) using repeated squaring
func modPower(base, exponent, modulus *big.Int) *big.Int {

	result := big.NewInt(1)
	exp := new(big.Int).Set(exponent)

	// Repeated squaring algorithm
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

func main() {
	// Connect to the RPC server
	client, err := rpc.Dial("tcp", "localhost:1234")
	if err != nil {
		log.Fatal("Error connecting to RPC server:", err)
	}
	defer client.Close()

	oracleClient := &OracleClient{client: client}

	// Get the public key from oracle
	publicKey, err := oracleClient.GetPublicKey()

	if err != nil {
		log.Fatal("Error calling Get public key method:", err)
	}

	// The public key
	modulus := publicKey.PublicKey.N
	publicExponent := publicKey.PublicKey.E

	// Compute 2**e mod N, it will be used later to compute the encryption of next message
	powerOfTwo := modPowerofTwo(publicExponent, modulus)

	// Test case for a message in the second half
	//bar := new(big.Int).Div(modulus, big.NewInt(2))
	//mes := new(big.Int).Add(bar, big.NewInt(20))

	// Choose initial m
	mes := big.NewInt(30)

	fmt.Println("mes:", mes)

	var cipher *big.Int
	// Compute the encryption of m
	cipher = modPower(mes, big.NewInt(int64(publicExponent)), modulus)

	var min *big.Int
	var max *big.Int
	var tmp *big.Int

	// Search from 0 to N - 1
	min = big.NewInt(0)
	max = new(big.Int).Set(modulus)

	var reply LocReply
	var isInFirstHalf bool
	var args LocArgs

	//Binary search using loc function to find the decryption of cipher
	for min.Cmp(max) < 0 {

		// Ask Oracle for the loc of cipher
		args = LocArgs{Cipher: cipher}
		err = oracleClient.Loc(args, &reply)

		if err != nil {
			log.Fatal("Error calling Loc function:", err)
		}

		isInFirstHalf = reply.IsInFirstHalf

		if isInFirstHalf {
			// When the cipher is in the first half, decrease the max to the middle of search space
			tmp = new(big.Int).Sub(max, min)
			tmp = new(big.Int).Div(tmp, big.NewInt(2))
			max = new(big.Int).Add(tmp, min)
		} else {
			// When it's in second half, make min equal to the middle of search space
			tmp = new(big.Int).Sub(max, min)
			tmp = new(big.Int).Add(tmp, big.NewInt(1))
			tmp = new(big.Int).Div(tmp, big.NewInt(2))
			min = new(big.Int).Add(tmp, min)
		}

		// Compute the encryption for the double of the previous plain message
		cipher = new(big.Int).Mul(cipher, powerOfTwo)
		cipher = new(big.Int).Mod(cipher, modulus)

		reply.IsInFirstHalf = false
	}

	// Print the decryption of initial cipher
	fmt.Println("dec:", min)

}
