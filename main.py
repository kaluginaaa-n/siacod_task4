import tkinter as tk


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        word = word.lower()
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.frequency += 1

    def _search_with_prefix(self, node, prefix):
        results = []

        def dfs(current_node, current_word):
            if current_node.is_end_of_word:
                results.append((current_word, current_node.frequency))
            for char, child_node in current_node.children.items():
                dfs(child_node, current_word + char)

        dfs(node, prefix)
        return results

    def get_suggestions(self, prefix, max_suggestions):
        prefix = prefix.lower()
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        results = self._search_with_prefix(node, prefix)
        results.sort(key=lambda x: -x[1])  # Сортируем по убыванию частоты
        return [word for word, _ in results[:max_suggestions]]


class AutocompleteApp:
    def __init__(self, max_suggestions=7):
        self.trie = Trie()
        self.max_suggestions = max_suggestions

        self.root = tk.Tk()
        self.root.title("Автодополнение")

        self.input_field = tk.Entry(self.root, font=("Arial", 14), width=20)
        self.input_field.pack(padx=20, pady=20)
        self.input_field.bind("<KeyRelease>", self.update_suggestions)

        self.add_button = tk.Button(self.root, text="Добавить слово", command=self.add_word, font=("Arial", 14), width=20, bg="peachpuff")
        self.add_button.pack()

        self.suggestions_label = tk.Label(self.root, text="Предложения:", font=("Arial", 14))
        self.suggestions_label.pack()

        self.suggestions_list = tk.Listbox(self.root, font=("Arial", 14), width=20, height=20)
        self.suggestions_list.pack(padx=20, pady=20)

    def add_word(self):
        word = self.input_field.get().strip()
        if word:
            self.trie.insert(word)
            self.input_field.delete(0, tk.END)
            self.update_suggestions()

    def update_suggestions(self, event=None):
        prefix = self.input_field.get().strip().lower()
        suggestions = self.trie.get_suggestions(prefix, self.max_suggestions)
        self.suggestions_list.delete(0, tk.END)
        for suggestion in suggestions:
            self.suggestions_list.insert(tk.END, suggestion)

    def run(self):
        self.root.mainloop()


app = AutocompleteApp()
app.run()
