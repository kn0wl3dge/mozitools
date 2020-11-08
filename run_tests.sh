source venv/bin/activate
mkdir /tmp/mozi-decoder-test
cp ./test/samples/* /tmp/mozi-decoder-test/
ls -la /tmp/mozi-decoder-test/
python -m pytest -vvv -s
rm -rf /tmp/mozi-decoder-test