Tests=("test0" "test1" "test2" "test3" "test4" "test5")
for t in ${Tests[*]}; do
    echo "compiling test $t"
    python3 main.py tests/${t}/${t}.cpp > tests/${t}/${t}ir.cpp
    cd tests/$t
    echo "compiling"
    make
    echo ""
    echo "running original, result:"
    ./original
    echo ""
    echo "running compiled, result:"
    ./compiled
    echo ""
    echo "----------"
    cd ../../
done
