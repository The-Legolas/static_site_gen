# Remember to comment out the correct thing in src/main.py

python3 -m src.main "$@"
cd public && python3 -m http.server 8888
