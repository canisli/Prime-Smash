def sgn(x):
   return int(x>0)

def is_prime(n):
  """O(sqrt(n)) primality checker using the fact that all primes > 3 are in the form 6n±1
  https://stackoverflow.com/a/15285588/10637448"""
  if n == 1: return False  
  if n == 2 or n == 3: return True
  if n < 2 or n%2 == 0: return False
  if n < 9: return True
  if n%3 == 0: return False
  r = int(n**0.5)
  # since all primes > 3 are of the form 6n ± 1
  # start with f=5 (which is prime)
  # and test f, f+2 for being prime
  # then loop by 6. 
  f = 5
  while f <= r:
    print('\t',f)
    if n % f == 0: return False
    if n % (f+2) == 0: return False
    f += 6
  return True 

def factorize_composite(n):
    """Return an array of factors EXECPT 1 and n"""
    from functools import reduce

    return set(reduce(list.__add__, 
            ([i, n//i] for i in range(2, int(n**0.5) + 1) if n % i == 0)))