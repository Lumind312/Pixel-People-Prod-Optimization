CPPFLAGS=-Wall -Werror -Wuninitialized -O2

calculate.exe: main.o Cluster.o CSVReader.o Prints.o
	g++ main.o Cluster.o CSVReader.o Prints.o -o calculate.exe $(CPPFLAGS)

Prints.o: Prints.h Prints.cpp
	g++ Prints.cpp -c $(CPPFLAGS)
CSVReader.o: CSVReader.h CSVReader.cpp
	g++ CSVReader.cpp -c $(CPPFLAGS)
Cluster.o: Cluster.h Cluster.cpp 
	g++ Cluster.cpp -c $(CPPFLAGS)
main.o: main.cpp 
	g++ main.cpp -c $(CPPFLAGS)

clean:
	rm *.o

# g++ main.cpp CSVReader.cpp Cluster.cpp Prints.cpp -O2 -o calculate.exe -Wall -Werror -Wuninitialized