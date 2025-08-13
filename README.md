<img width="50%" height="50%" alt="carbon" src="https://github.com/user-attachments/assets/cc04b122-1012-486b-aec1-de113f51ab53" />

# Chinese-Quick-Input-checking-Terminal

Chinese-Quick-Input-checking-Terminal is a terminal application for querying Cangjie/Quick input codes for Chinese characters, with interactive training mode.

## Features

- Query Cangjie/Quick input codes for Chinese characters, with root hints
- Training mode: randomly pick a character, enter the code, and get instant feedback
- Combo counter: consecutive correct answers will show your combo streak, wrong answers reset the combo
- Dynamic weighted random: characters you get wrong more often will appear more frequently, while those you get right will appear less
- Lightweight and easy to use

## Installation

```powershell
git clone https://github.com/SouirTommer/Chinese-Quick-Input-checking-Terminal
cd Chinese-Quick-Input-checking-Terminal
```

## Usage

```powershell
python app.py
```

After starting, you can select the query mode:
- 1 = Quick (show only first and last code)
- 2 = Cangjie (show full code)

Query: Just enter Chinese characters to display their codes and root hints.

Training mode: Enter `/train` to start training. Follow the prompts to enter the code for each character. Consecutive correct answers will show your combo, wrong answers reset the combo. The probability of each character appearing is automatically adjusted based on your performance.

Change query mode: Enter `/setting`

Exit training mode: Enter `/exit`

## Data Source

Code mapping data is from [chauchakching/chinese-quick-mapping](https://github.com/chauchakching/chinese-quick-mapping).

## Contribution

Feel free to open issues or pull requests to improve this project!

## License

MIT License
