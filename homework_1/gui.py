import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout,
    QWidget, QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt


class WordCounterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Счётчик слов и символов")
        self.setGeometry(100, 100, 400, 200)

        # Центральный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Поле для ввода текста
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Введите или вставьте текст сюда...")
        self.text_edit.textChanged.connect(self.update_stats)
        layout.addWidget(self.text_edit)

        # Панель статистики
        stats_layout = QHBoxLayout()

        self.label_chars_with_spaces = QLabel("Символов (с пробелами): 0")
        self.label_chars_without_spaces = QLabel("Символов (без пробелов): 0")
        self.label_words = QLabel("Слов: 0")
        self.label_longest_word = QLabel("Самое длинное слово: —")

        # Стилизация меток
        for label in [self.label_chars_with_spaces, self.label_chars_without_spaces,
                      self.label_words, self.label_longest_word]:
            label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    padding: 8px;
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    border-radius: 6px;
                    margin: 2px;
                }
            """)
        stats_layout.addWidget(self.label_chars_with_spaces)
        stats_layout.addWidget(self.label_chars_without_spaces)
        stats_layout.addWidget(self.label_words)
        stats_layout.addWidget(self.label_longest_word)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        self.update_stats()

    def update_stats(self):
        text = self.text_edit.toPlainText()
        # 1. Символы с пробелами
        chars_with_spaces = len(text)
        # 2. Символы без пробелов
        chars_without_spaces = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))
        # 3. Количество слов (разделяем по пробельным символам)
        words = text.split()
        word_count = len(words)
        # 4. Самое длинное слово
        if words:
            longest_word = max(words, key=len)
            longest_word_display = longest_word if len(longest_word) <= 30 else longest_word[:27] + "..."
        else:
            longest_word_display = "—"
        # Обновляем метки
        self.label_chars_with_spaces.setText(f"Символов (с пробелами): {chars_with_spaces}")
        self.label_chars_without_spaces.setText(f"Символов (без пробелов): {chars_without_spaces}")
        self.label_words.setText(f"Слов: {word_count}")
        self.label_longest_word.setText(f"Самое длинное слово: {longest_word_display}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = WordCounterApp()
    window.show()
    sys.exit(app.exec())
