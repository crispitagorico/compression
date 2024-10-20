# Huffman Tree


# Arithmetic Coding

Arithmetic coding, also known as range coding, is an example of **streaming codes**. Unlike symbol codes, streaming codes assign codewords to entire messages rather than individual symbols. 

The core idea is to associate each symbol with a **subinterval** of the interval $$[0,1]$$, where the length of the subinterval corresponds to the symbol's probability. When encoding a sequence, subsequent symbols are represented as subintervals of the previous symbol’s interval, proportional to their joint probability.

For example:
- If symbol "a" has a probability of $$ \frac{1}{5} $$ and is assigned to the interval $$[0, 0.2)$$, 
- The sequence "aa" would be encoded as $$[0, 0.04)$$.

This process iterates over the entire sequence, producing nested subintervals. Any real number within the final subinterval uniquely identifies the sequence.

## Efficiency

In practice, the **final subinterval**'s length reflects the **sequence’s joint probability**, and the smallest number of bits needed to represent a number within this interval encodes the message. The code length approximates the $$-\log_2 P(\text{sequence}) $$, consistent with entropy.

Let $$ x_n $$ be a message of length $$ n $$ and $$ C(x_n) $$ its codeword, under an assumed probability distribution $$ Q $$. The length of the code $$ |C(x_n)| $$ satisfies:

$$ |C(x_n)| < \lceil -\log_2 Q(x_n) \rceil + 1 $$

If the true distribution is $$ P $$, the average code length is bounded by $$ H[P,Q] + 2 $$. Unlike Huffman coding, arithmetic coding’s overhead is spread across all symbols, achieving greater efficiency for long messages. Per symbol, the overhead is approximately $$ \frac{2}{n} $$ bits compared to Huffman coding’s 1 bit per symbol.

### First-In-First-Out Structure

Arithmetic coding implements a **first-in-first-out (FIFO)** data structure, meaning symbols encoded first are also decoded first. This makes it especially useful in compression methods that involve autoregressive models.


# Asymmetric Numeral Systems (ANS)

Another example of a streaming code is **asymmetric numeral systems (ANS)**. While arithmetic coding operates as a queue (FIFO), ANS functions as a **stack** or **last-in-first-out (LIFO)** structure, where the last symbol encoded is the first to be decoded.

## Concept

Numeral systems like decimal or binary are optimal codes for uniform distributions over a finite alphabet. They encode a sequence of symbols into a single integer, called the **stack**. 

- **Encoding:** Multiply the stack by the base (e.g., 2 or 10) and add the symbol.
- **Decoding:** Recover the symbol as the stack modulo the base, and reduce the stack by dividing it by the base.

The length of the stack, in binary, approximates the number of symbols multiplied by the logarithm of the numeral system's base, consistent with entropy coding.

### ANS Generalization

ANS extends this concept to **non-uniform probability distributions**. Symbols are mapped to subintervals of the unit interval, and this interval is discretized using a fine grid. Each point in the grid corresponds to a symbol, forming a new alphabet that can be encoded with a numeral system. Although there is redundancy in encoding, ANS avoids this through **bits-back coding**.

Like arithmetic coding, ANS incurs an overhead of up to 2 bits per message.
