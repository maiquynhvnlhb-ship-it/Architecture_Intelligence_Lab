<<<<<<< HEAD
class HealthExpertSystem:
    def __init__(self):
        self.knowledgeBase ={
            "sốt": {
                "question": "Nhiệt độ cơ thể bạn có trên 38°C không?",
                "có": "sốt_cao",
                "không": "sốt_nhẹ"
            },
            "sốt_cao": {
                "statement": "Sốt cao: Nên đi khám bác sĩ sớm, uống thuốc hạ sốt nếu cần và bù nước đầy đủ"
            },
            "sốt_nhẹ": {
                "statement": "Sốt nhẹ: Nghỉ ngơi, uống nhiều nước ấm, theo dõi nhiệt độ thường xuyên"
            },
            "ho": {
                "question": "Bạn ho có đờm hay ho khan?",
                "có đờm": "ho_đờm",
                "ho khan": "ho_khan"
            },
            "ho_đờm": {
                "statement": "Ho có đờm: Có thể viêm họng/viêm phế quản. Súc miệng nước muối, tránh đồ lạnh. Nếu kéo dài nên đi khám"
            },
            "ho_khan": {
                "statement": "Ho khan: Có thể do dị ứng hoặc viêm họng. Uống mật ong ấm, tránh bụi và khói thuốc"
            },
            "đau_bụng": {
                "question": "Đau ở vùng trên rốn không?",
                "có": "đau_bụng_trên",
                "không": "đau_bụng_dưới"
            },
            "đau_bụng_trên": {
                "question": "Có ợ chua hoặc buồn nôn không?",
                "có": "viêm_dạ_dày",
                "không": "đau_bụng_trên_khác"
            },
            "viêm_dạ_dày": {
                "statement": "Có thể viêm dạ dày: Ăn nhẹ, tránh đồ cay nóng"
            },
            "đau_bụng_trên_khác": {
                "statement": "Đau bụng trên: Theo dõi thêm, nếu đau nhiều nên đi khám"
            },
            "đau_bụng_dưới": {
                "question": "Có tiêu chảy không?",
                "có": "rối_loạn_tiêu_hóa",
                "không": "đau_bụng_dưới_khác"
            },
            "rối_loạn_tiêu_hóa": {
                "statement": "Rối loạn tiêu hóa: Uống oresol, ăn thức ăn nhẹ"
            },
            "đau_bụng_dưới_khác": {
                "statement": "Đau bụng dưới: Nếu đau nhiều cần kiểm tra thêm"
            }
        }
        def start(self):
            print("😀👉HỆ CHUYÊN GIA SỨC KHOỎE ĐƠN GIẢN👈😀")
            print("Bạn đang gặp vâ đề gì (sốt, ho, đau bụng)?")
            choice = input("Bạn đang gặp vâ đề gì (sốt, ho, đau bụng):  ")
            if choice in self.knowledgeBase:
                self.evaluate(choice)
            else:
                print("Xin lỗi, tôi chưa thể giải quyết tình trạng này 🙁")
        def evaluate(self, problem):
            for step in self.knowledgeBase[problem]:
                if "question" in step:
                    answer = input(step["question"]+ "(có/không): ").lower()
                    if answer == "có":
                        self.evaluate(step["có"])
                    else:
                        self.evaluate(step["không"])
                    return
                elif "statement" in step:
                    print("\nKết luận: "+step["statement"])
                    return
# Chạy code
if __name__ == '__main__':
    exp = HealthExpertSystem()
    exp.start()
=======
#Phần cơ sở tri thức
class HealthExpertSystem:
    def __init__(self):
        self.knowledgeBase = {
            "sốt": {
                "question": "Chat: Nhiệt độ cơ thể bạn có trên 38°C không?(có/không)",
                "có": "sốt cao",
                "không": "sốt nhẹ"
            },
            "sốt cao": {
                "statement": "Sốt cao, nên đi khám bác sĩ sớm, uống thuốc hạ sốt nếu cần và bù nước đầy đủ"
            },
            "sốt nhẹ": {
                "statement": "Sốt nhẹ, nghỉ ngơi, uống nhiều nước ấm, theo dõi nhiệt độ thường xuyên"
            },
            "ho": {
                "question": "Chat: Bạn ho có đờm hay ho khan?",
                "có đờm": "ho đờm",
                "ho khan": "ho khan"
            },
            "ho đờm": {
                "statement": "Ho có đờm, có thể viêm họng/viêm phế quản. Súc miệng nước muối, tránh đồ lạnh. Nếu kéo dài nên đi khám"
            },
            "ho khan": {
                "statement": "Ho khan, có thể do dị ứng hoặc viêm họng. Uống mật ong ấm, tránh bụi và khói thuốc"
            },
            "đau bụng": {
                "question": "Chat: Đau ở vùng trên rốn không?(có/không)",
                "có": "đau bụng trên",
                "không": "đau bụng dưới"
            },
            "đau bụng trên": {
                "question": "Chat: Có ợ chua hoặc buồn nôn không?",
                "có": "viêm dạ dày",
                "không": "đau bụng trên khác"
            },
            "viêm dạ dày": {
                "statement": "Có thể viêm dạ dày, ăn nhẹ, tránh đồ cay nóng"
            },
            "đau bụng trên khác": {
                "statement": "Đau bụng trên, theo dõi thêm, nếu đau nhiều nên đi khám"
            },
            "đau bụng dưới": {
                "question": "Chat: Có tiêu chảy không?",
                "có": "rối loạn tiêu hóa",
                "không": "đau bụng dưới khác"
            },
            "rối loạn tiêu hóa": {
                "statement": "Rối loạn tiêu hóa, uống oresol, ăn thức ăn nhẹ"
            },
            "đau bụng dưới khác": {
                "statement": "Đau bụng dưới, nếu đau nhiều cần kiểm tra thêm"
            }
        }

# Máy suy luận
    def evaluate(self, problem):
        node = self.knowledgeBase[problem]
        # Nếu node là 1 câu hỏi
        if "question" in node:
            print(node["question"])
            answer = input("Bạn: ").lower()
            if answer in node:
                self.evaluate(node[answer])
            else:
                print("Chat: Câu trả lời không hợp lệ 🙁")
        # Nếu node là kết luận
        elif "statement" in node:
            print("Chat: " + node["statement"])


#Code chính
    def start(self):
        print("😀👉 HỆ CHUYÊN GIA SỨC KHOẺ ĐƠN GIẢN 👈😀")
        self.question()

    def question(self):
        print("Chat: Bạn đang gặp vấn đề gì (sốt, ho, đau bụng)?")
        choice = input("Bạn: ").lower()
        if choice in self.knowledgeBase:
            self.evaluate(choice)
        else:
            print("Chat: Xin lỗi, tôi chưa thể giải quyết tình trạng này 🙁")
        self.repeat()

    def repeat(self):
        print("Chat: Bạn có vấn đề gì về sức khỏe cần hỏi không?")
        choice = input("Bạn: ").lower()
        if choice == "có":
            self.question()
        elif choice =="không":
            return
        else:
            print("Chat: Trả lời có hay không đi ạ😗")
            self.repeat()

# Chạy code
if __name__ == '__main__':
    exp = HealthExpertSystem()
    exp.start()

>>>>>>> e8dbfaa (update)
