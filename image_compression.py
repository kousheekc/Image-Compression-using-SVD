import cv2
import numpy as np
import math

def get_u(v, sigma):
    u = []
    for i in range(len(v)):
        ui = (1/sigma[i])*np.dot(A_float64, v[:,i])
        u.append(ui)
        
    return np.transpose(np.array(u))


def get_v(u, sigma):
    v = []
    for i in range(len(u)):
        vi = (1/sigma[i])*np.dot(A_float64.transpose(), u[:,i])
        v.append(vi)

    return np.transpose(np.array(v))


def recreate_approx_image(sigma, u, v, k):
    B = np.zeros((m,n))
    A_hat = np.zeros((m, n), dtype=np.uint8)

    for i in range(k):
        B = np.add(B, sigma[i]*np.outer(u[:, i], v[:, i]))

    for i in range(len(B)):
        for j in range(len(B[0])):
            if B[i][j] > 255:
                A_hat[i][j] = 255
            elif B[i][j] < 0:
                A_hat[i][j] = 0
            else:
                A_hat[i][j] = B[i][j]
                
    return A_hat


def get_error(A, A_hat):
    B = A - A_hat
    return math.sqrt(np.dot(B.transpose(), B).trace())

        
A = cv2.imread("assets\img1.jpg")
A = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
A_float64 = np.array(A, dtype=np.float64)

k = 5

m = np.shape(A_float64)[0]  
n = np.shape(A_float64)[1]

print("row = ", m)
print("col = ", n)

if (m > n):
    AtA = np.dot(A_float64.transpose(),A_float64)
    sigma, v = np.linalg.eig(AtA)
    u = get_u(v, sigma)
    
##    print(type(AAt[0][0]))
##    print("eigenvalue ", type(sigma[0]))
##    print("v ", type(v[0][0]))
##    print("u ", type(u[0][0]))
##    print("eigenvalues: ", sigma)
##    print("number of eigenvalues: ", len(sigma))
##    print("u: ", u)
##    print("number of uis: ", len(u))
##    print("v: ", v)
##    print("number of vis: ", len(v))
    
    
else:
    AAt = np.dot(A_float64, A_float64.transpose())
    sigma, u = np.linalg.eig(AAt)
    v = get_v(u, sigma)
    
##    print(type(AAt[0][0]))
##    print("eigenvalue ", type(sigma[0]))
##    print("v ", type(v[0][0]))
##    print("u ", type(u[0][0]))
##    print("eigenvalues: ", sigma)
##    print("number of eigenvalues: ", len(sigma))
##    print("u: ", u)
##    print("number of uis: ", len(u))
##    print("v: ", v)
##    print("number of vis: ", len(v))



A_hat = recreate_approx_image(sigma, u, v, k)
error = get_error(A_float64, A_hat)
print(error)

cv2.imshow("A", A)
cv2.imshow("A_hat", A_hat)

cv2.imwrite('original.png', A)
cv2.imwrite('compressed{}.png'.format(k), A_hat)


cv2.waitKey(0)
cv2.destroyAllWindows()
