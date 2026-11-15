En este primer ejercicio se han creado dos funciones:
- `is_palindrome`: Recibe un string llamado palabra, crea dos indices que recorren la palabra; uno desde 0 y otro desde su final. Mientras ambos indices no coincidan (llega al centro de la palabra), el while se sigue ejecutan comprobando letra a letra que estas coincidan en ambos extremos de la palabra. Si no coinciden en alguno de estos casos, la variable que se devolverá, palindrome, pasa a ser False.

- `palidromes`: Aquí simplemente se devuelve un map de `is_palindrome` con la lista de palabras convertido en una lista.
