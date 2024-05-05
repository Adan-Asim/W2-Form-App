import unittest
import json
from app import app, db
import os


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        dummy_pdf_file = "test_w2_form.pdf"
        if os.path.exists(dummy_pdf_file):
            os.remove(dummy_pdf_file)

    def test_signup(self):
        response = self.app.post(
            "/api/user/signup",
            json={"email": "test@example.com", "name": "Test User", "password": "testpass"},
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "User created successfully")

        # Test duplicate signup
        response = self.app.post(
            "/api/user/signup",
            json={"email": "test@example.com", "name": "Another Test User", "password": "testpass2"},
        )
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "A user already exists with these details")

    def test_login(self):
        response = self.app.post(
            "/api/user/signup",
            json={"email": "test@example.com", "name": "Test User", "password": "testpass"},
        )
        self.assertEqual(response.status_code, 201)

        response = self.app.post(
            "/api/user/login",
            json={"email": "test@example.com", "password": "testpass"},
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("access_token", data)

        # Test invalid login
        response = self.app.post(
            "/api/user/login",
            json={"email": "test@example.com", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "Unable to log in, make sure given credentials are correct")

    def test_logout(self):
        response = self.app.post(
            "/api/user/signup",
            json={"email": "test@example.com", "name": "Test User", "password": "testpass"},
        )
        self.assertEqual(response.status_code, 201)

        response = self.app.post(
            "/api/user/login",
            json={"email": "test@example.com", "password": "testpass"},
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("access_token", data)
        access_token = data["access_token"]

        response = self.app.get(
            "/api/user/logout",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "User logout successful")

    
    def test_upload_file(self):
        def create_dummy_pdf(filename):
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas

            c = canvas.Canvas(filename, pagesize=letter)
            c.setFont("Helvetica", 12)

            text_content = [
                "W2 Form",
                "Employee Name: John Doe",
                "Employee ID: 123456",
                "Employer: XYZ Corporation",
                "Year: 2023",
                "Total Income: $50,000",
                "Taxes Paid: $10,000",
            ]
            
            y_position = 750
            for line in text_content:
                c.drawString(50, y_position, line)
                y_position -= 20

            c.save()

        response = self.app.post(
            "/api/user/signup",
            json={"email": "test@example.com", "name": "Test User", "password": "testpass"},
        )
        self.assertEqual(response.status_code, 201)

        response = self.app.post(
            "/api/user/login",
            json={"email": "test@example.com", "password": "testpass"},
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("access_token", data)
        access_token = data["access_token"]

        create_dummy_pdf("test_w2_form.pdf")
        with open("test_w2_form.pdf", "rb") as f:
            response = self.app.post(
                "/api/file/upload",
                data={"file": (f, "test_w2_form.pdf")},
                headers={"Authorization": f"Bearer {access_token}"},
            )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "File uploaded and parsed successfully")


    def test_get_user_chat_history(self):
        def populate_chat_history():
            from model import User, W2Form, ChatHistory
            from datetime import datetime

            user = User.query.filter_by(email="test@example.com").first()

            w2_form = W2Form(user_id=user.id, filename="test_w2_form.pdf", data={"year": 2024, "total_income": 50000, "taxes_paid": 10000})
            db.session.add(w2_form)
            db.session.commit()

            chat_entries = [
                {
                    "user_id": user.id,
                    "w2_form_id": w2_form.id,
                    "user_query": "How much did I earn last year?",
                    "ai_response": "Your total earnings last year were $50,000.",
                    "timestamp": datetime(2023, 1, 15, 10, 30, 0),
                },
                {
                    "user_id": user.id,
                    "w2_form_id": w2_form.id,
                    "user_query": "Show me my tax deductions.",
                    "ai_response": "Your tax deductions are $10,000.",
                    "timestamp": datetime(2023, 1, 16, 12, 15, 0),
                },
            ]

            for entry in chat_entries:
                chat = ChatHistory(**entry)
                db.session.add(chat)
            
            db.session.commit()
            
        response = self.app.post(
            "/api/user/signup",
            json={"email": "test@example.com", "name": "Test User", "password": "testpass"},
        )
        self.assertEqual(response.status_code, 201)

        response = self.app.post(
            "/api/user/login",
            json={"email": "test@example.com", "password": "testpass"},
        )

        populate_chat_history()

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("access_token", data)
        access_token = data["access_token"]

        response = self.app.get("/api/user/chat-history", headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn("chat_history_by_w2_form", data)
        chat_history = data["chat_history_by_w2_form"]

        self.assertEqual(len(chat_history), 1)
        self.assertEqual(chat_history[0]["filename"], "test_w2_form.pdf")
        self.assertEqual(len(chat_history[0]["chat_history"]), 2)

        first_chat = chat_history[0]["chat_history"][0]
        self.assertEqual(first_chat["user_query"], "How much did I earn last year?")
        self.assertEqual(first_chat["ai_response"], "Your total earnings last year were $50,000.")

        second_chat = chat_history[0]["chat_history"][1]
        self.assertEqual(second_chat["user_query"], "Show me my tax deductions.")
        self.assertEqual(second_chat["ai_response"], "Your tax deductions are $10,000.")


if __name__ == "__main__":
    unittest.main()
