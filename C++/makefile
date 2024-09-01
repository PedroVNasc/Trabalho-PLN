all : main.o treemap.o utils.o
	clang++-18 -std=c++20 utils.o treemap.o main.o -o main

encoding : encoding.o utils.o
	clang++-18 -std=c++20 utils.o encoding.o -o encoding

treemap.o : treemap.cpp treemap.hpp
	clang++-18 -std=c++20 treemap.cpp -c

utils.o : utils.cpp utils.hpp
	clang++-18 -std=c++20 utils.cpp -c

encoding.o : encoding.cpp utils.hpp
	clang++-18 -std=c++20 encoding.cpp -c

main.o : main.cpp treemap.hpp utils.hpp
	clang++-18 -std=c++20 main.cpp -c

run :
	./main

clean :
	rm main
	rm *.o
