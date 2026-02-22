#include<iostream>
#include <vector>
#include <cstdint>
#include <iomanip>

using namespace std;

class LFSR {
    uint32_t state;
    uint32_t polynomial;
    int length;

    public:
    LFSR(uint32_t seed, uint32_t poly, int len){
        state = seed; 
        polynomial = poly;
        length = len;  
        
        if (seed == 0){
            cout << "invalid seed value"<< endl;
        }
    }
    
    int next_bit(){
        int output = state & 1U;
        uint32_t feedback = state & polynomial;
        int parityResult = __builtin_parity(feedback);
        state = state >> 1;
        int pos = length - 1;
        int shift = parityResult << pos;
        state = shift | state;
        return output;
    }
    
    vector<int> generate(int num_bits){
    vector<int> stream;
    for (int i = 0; i < num_bits; i++) {
    stream.push_back(next_bit());
    }
    return stream;


    }
    uint32_t get_state(){
        
        return state;
    } 
};


int main(){

    LFSR f1(0b1001, 0b10011, 4);
    LFSR f2(0b1001, 0b10011, 4);
    LFSR f3(0, 0b10011, 4);

    f1.next_bit();
    vector<int> result = f1.generate(15);
    for (int bit : result) {
        cout << bit;
    }
    cout<< endl;

    f2.next_bit();
    vector<int> result2 = f2.generate(30);
    for (int bit : result2) {
        cout << bit;
    }

    cout << endl;

}
