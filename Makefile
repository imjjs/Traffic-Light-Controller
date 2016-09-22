CC=g++
BUILD = ./build

all: libtest.so

init:
	mkdir $(BUILD)

clean:
	rm -rf $(BUILD)
	rm -f libtest.so


test.o: init test.cpp config.hpp Intersection.hpp
	$(CC) -std=c++11 -c -fPIC -o $(BUILD)/test.o test.cpp

intersection.o: init Intersection.cpp Intersection.hpp config.hpp
	$(CC) -std=c++11 -c -I json/include -fPIC -o $(BUILD)/intersection.o Intersection.cpp

json.o: init json/jsoncpp.cpp
	$(CC) -std=c++11 -c -I json/include -fPIC -o $(BUILD)/json.o json/jsoncpp.cpp

libtest.so: test.o intersection.o json.o
	$(CC) -shared -fPIC -o $(BUILD)/libtest.so $(BUILD)/test.o $(BUILD)/intersection.o $(BUILD)/json.o
