#include <iostream>
#include <vector>
#include <cstdint>
#include <iomanip>
#include <cstdint>
#include <cstring>
#include <random>
#include <utility>
#include <cmath>


using namespace std;

class secret{

    // secret D
    uint32_t D = 0;

    // threshold k
    int k = 0;

    // shares
    int n;

    // prime
    int p = 0;

    // coefficients
    vector<uint32_t> coefficient;
    public:
    secret(uint32_t a, int b, int c, int d){
        D = a;
        n = b;
        k = c;
        p = d;

        if (p< D && p<n){
            cout << "Invalid input for either schemes" << endl;
        }
    }

    void threshold_scheme(int s){
        s = k;
        
        coefficient.resize(k);
        
        random_device rd;
        mt19937 gen(rd());
        coefficient[0] = D;
        
        for(int i=0; i<k-1; i++){
            uniform_int_distribution<uint32_t> distrib(0, p);
            uint32_t random_coeff = distrib(gen);
            coefficient.push_back(random_coeff);
    }
    }

    int evaluate_poly(vector<uint32_t> a, int x, int po){
    uint64_t result = 0;
    for (size_t power = 0; power < coefficient.size(); ++power) {
        result = (result + coefficient[power] * mod_pow(x, power, p)) % p;
    }
    
    }

    uint32_t modular_inverse(uint32_t a, uint32_t b){
        uint32_t c = (uint32_t)pow(a,(p-2)) % p;
        return c;
        }

    vector<uint32_t> shares(){
        vector<uint32_t> shares;
        shares.resize(1);
        shares[0] = 0;
        for(int i=1; i<=n; i++){
            uint32_t value = evaluate_poly(coefficient, i, p);
            shares.push_back(value);
        }
        return shares;
}

    uint32_t mod_pow(uint32_t base, uint32_t exp, uint32_t mod) {
        uint32_t result = 1;
        base %= mod;
        while (exp > 0) {
            if (exp % 2 == 1) {
                result = (result * base) % mod;
            }
            base = (base * base) % mod;
            exp /= 2;
        }
        return result;
    }

    uint32_t reconstruct(uint32_t b, int a){
        uint32_t secret = 0;
        vector<pair<int,int>> k_shares;
        size_t len = k_shares.size();
        for(int i=0; i<len ;i++){
            uint32_t xi = k_shares[i].first;
            uint32_t yi = k_shares[i].second;
        int numerator = 1;
        int denominator = 1;
        for(int j=0; j<len; j++ ){
            if (i==j){
                continue;
                uint32_t xj = k_shares[j].first;
                uint32_t yj = k_shares[j].second;
                numerator *= (0-xj);
                denominator *= (xi - xj);
                }
            }   
        uint32_t lagrange_coeff = yi* numerator * modular_inverse(denominator, p);
        secret+= lagrange_coeff;
        }
    uint32_t d = secret %p;
    return d;
    }

};

