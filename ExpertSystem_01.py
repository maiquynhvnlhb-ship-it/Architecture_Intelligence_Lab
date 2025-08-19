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