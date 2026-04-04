#include <iostream>
#include <string>
#include <vector>
#include <unordered_set>
#include <string>
#include <unordered_map>
#include <cctype>

using namespace std;

class Playfair_Cipher{

    private: 
        string plaintext;
        vector <string> ciphertext;
        string key;
        int len, len_p;
        char grid_dimension[5][5];
        unordered_map<char, pair<int,int>> lookup;
        vector<string> diagraph;

    public:
        // constructor:
        Playfair_Cipher(string a, string b){
            plaintext = a;

            string cln_key;
            for (char ch : b) {
                if (isalpha(static_cast<unsigned char>(ch))) {
                    char up = static_cast<char>(toupper(static_cast<unsigned char>(ch)));
                        if (up == 'J') up = 'I';
                            cln_key.push_back(up);
                }
            }

            vector<char> unique_key = brute(cln_key);
            key.assign(unique_key.begin(), unique_key.end());
            len = key.size();

            string cln_px;
                for(char ch1 : a) {
                    if (isalpha(static_cast<unsigned char>(ch1))) {
                        char u = static_cast<char>(toupper(static_cast<unsigned char>(ch1)));
                            if (u == 'J') u = 'I';
                                cln_px.push_back(u);
                    }
                }
                plaintext = cln_px;
                len_p = plaintext.size();
        }
    
        vector <char> brute(const string& s){
            vector <char> result;
            for (char ch : s){
                bool found = false;
                    for (char r: result){
                        if (r == ch){
                            found = true;
                                break;
                        }
                    }
                    if(!found){
                        result.push_back(ch);
                    }
                }
                return result;
        }

        void Grid_Convert(){
            
            string full_table = key;
            string alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"; 

            for (char ch : alphabet) {
                if (full_table.find(ch) == string::npos) {
                    full_table.push_back(ch);
                }
            }

            for (int i = 0; i < 25; i++) {
                int row = i / 5;
                    int column = i % 5;
                        grid_dimension[row][column] = full_table[i];
                        lookup[full_table[i]] = {row, column};
            }

            cout << "The grid is: \n";
                for (int i=0; i< 5; i++){
                    for(int j=0; j<5; j++){
                        cout<< grid_dimension[i][j] << " ";
                    }
                    cout << "\n";
                }
        }

        void plaintxt(){
            diagraph.clear();
            int i = 0;

            while (i < len_p) {
                if (i + 1 >= len_p) {
                    string pair = "";
                    pair += plaintext[i];
                    pair += 'X';
                    diagraph.push_back(pair);
                    i += 1; // important
                }
                else if (plaintext[i] == plaintext[i + 1]) {
                    string pair = "";
                    pair += plaintext[i];
                    pair += 'X';
                    diagraph.push_back(pair);
                    i += 1; // important: only advance one char here
                }
                else {
                    string pair = "";
                    pair += plaintext[i];
                    pair += plaintext[i + 1];
                    diagraph.push_back(pair);
                    i += 2;
                }
            }
        }

        void encryption(){
            ciphertext.clear();

            for (const string& pair : diagraph) {
                char first = pair[0];
                char second = pair[1];

                auto pos1 = lookup[first];
                auto pos2 = lookup[second];

                string out = "";

                if (pos1.first == pos2.first) {
                    // same row -> move right
                    out += grid_dimension[pos1.first][(pos1.second + 1) % 5];
                    out += grid_dimension[pos2.first][(pos2.second + 1) % 5];
                }
                else if (pos1.second == pos2.second) {
                    // same column -> move down
                    out += grid_dimension[(pos1.first + 1) % 5][pos1.second];
                    out += grid_dimension[(pos2.first + 1) % 5][pos2.second];
                }
                else {
                    // rectangle -> swap columns
                    out += grid_dimension[pos1.first][pos2.second];
                    out += grid_dimension[pos2.first][pos1.second];
                }

                ciphertext.push_back(out);
            }

            cout << "Ciphertext: ";
            for (const string& p : ciphertext) cout << p;
            cout << "\n";
        }

};

int main(){
    Playfair_Cipher p1("cookies","ENCRYPT");
    p1.Grid_Convert();
    p1.plaintxt();
    p1.encryption();
}
