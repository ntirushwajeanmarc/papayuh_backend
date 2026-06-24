from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import datetime
import enum

class UserRole(str, enum.Enum):
    SUPER_ADMIN = "Super Admin"
    AKAGARI_ADMIN = "Akagari Admin"
    UMUDUGUDU_LEADER = "Umukuru w'Umudugudu"
    MUTWARASIBO = "Mutwarasibo"
    UMUTURAGE = "Umuturage"

class RequestStatus(str, enum.Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    REJECTED = "Rejected"

class RequestType(str, enum.Enum):
    MITUWELI = "Mituweli"
    IREMBO = "Irembo"
    CERTIFICATE = "Certificate Request"
    COMPLAINT = "Complaint"
    GENERAL_SUPPORT = "General Support"

class PendingMigration(Base):
    __tablename__ = "pending_migrations"
    id = Column(Integer, primary_key=True, index=True)
    migration_name = Column(String, unique=True, index=True)
    applied_at = Column(DateTime, default=datetime.datetime.utcnow)

# 1. User Management
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    phone = Column(String)
    role = Column(String, default=UserRole.UMUTURAGE.value)
    village = Column(String)
    cell = Column(String)
    sector = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# 2. Citizen Management
class Citizen(Base):
    __tablename__ = "citizens"
    id = Column(Integer, primary_key=True, index=True)
    national_id = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)
    village = Column(String)
    cell = Column(String)
    sector = Column(String)
    date_of_birth = Column(DateTime)
    gender = Column(String)
    registered_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Household(Base):
    __tablename__ = "households"
    id = Column(Integer, primary_key=True, index=True)
    head_id = Column(Integer, ForeignKey("citizens.id"))
    ubudehe_category = Column(String)
    house_type = Column(String)
    members_count = Column(Integer, default=1)
    address = Column(String)
    village = Column(String)
    cell = Column(String)
    sector = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# 3. Announcements
class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String)  # Inama z'abaturage, Umuganda, Gahunda za Leta
    author_id = Column(Integer, ForeignKey("users.id"))
    target_audience = Column(String)  # All, Village, Cell, Sector
    target_id = Column(String)  # specific village/cell/sector identifier
    push_notification = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# 4. Reports
class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    report_type = Column(String)  # Daily, Weekly, Monthly, Security, Community Development
    submitted_by = Column(Integer, ForeignKey("users.id"))
    submitted_to = Column(Integer, ForeignKey("users.id"))
    level = Column(String)  # Mutwarasibo, Umudugudu, Akagari
    status = Column(String, default="Submitted")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# 5. Citizen Requests
class CitizenRequest(Base):
    __tablename__ = "citizen_requests"
    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey("citizens.id"))
    request_type = Column(String)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default=RequestStatus.PENDING.value)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# 6. Smart Service Center
class ServiceRequest(Base):
    __tablename__ = "service_requests"
    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey("citizens.id"))
    service_type = Column(String)  # Mituweli Assistance, Irembo Services, Printing, Scanning, Internet Access
    description = Column(Text)
    status = Column(String, default="Pending")
    handled_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# 7. Emergency Alerts
class EmergencyAlert(Base):
    __tablename__ = "emergency_alerts"
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String, nullable=False)  # Fire, Security, Health, Disaster
    title = Column(String, nullable=False)
    description = Column(Text)
    severity = Column(String)  # Low, Medium, High, Critical
    location = Column(String)
    reported_by = Column(Integer, ForeignKey("users.id"))
    sms_sent = Column(Boolean, default=False)
    app_notified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# 8. Public WiFi Management
class WiFiSession(Base):
    __tablename__ = "wifi_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    hotspot_name = Column(String)
    device_mac = Column(String)
    data_used_mb = Column(Float, default=0.0)
    session_start = Column(DateTime, default=datetime.datetime.utcnow)
    session_end = Column(DateTime)
    is_active = Column(Boolean, default=True)

class WiFiHotspot(Base):
    __tablename__ = "wifi_hotspots"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)
    village = Column(String)
    cell = Column(String)
    sector = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# 9. Youth Hub
class Training(Base):
    __tablename__ = "trainings"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)  # Computer Skills, Coding, AI Training, Robotics
    instructor = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    capacity = Column(Integer)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class TrainingRegistration(Base):
    __tablename__ = "training_registrations"
    id = Column(Integer, primary_key=True, index=True)
    training_id = Column(Integer, ForeignKey("trainings.id"))
    citizen_id = Column(Integer, ForeignKey("citizens.id"))
    attendance_count = Column(Integer, default=0)
    certified = Column(Boolean, default=False)
    registered_at = Column(DateTime, default=datetime.datetime.utcnow)

# 10. Community Projects
class CommunityProject(Base):
    __tablename__ = "community_projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    budget_total = Column(Float)
    budget_spent = Column(Float, default=0.0)
    status = Column(String, default="Planned")  # Planned, In Progress, Completed, On Hold
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    village = Column(String)
    cell = Column(String)
    sector = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ProjectProgress(Base):
    __tablename__ = "project_progress"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("community_projects.id"))
    report = Column(Text)
    progress_percentage = Column(Float)
    reported_by = Column(Integer, ForeignKey("users.id"))
    reported_at = Column(DateTime, default=datetime.datetime.utcnow)

# 11. Village Communication
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    group_type = Column(String)  # individual, village, cell, sector
    group_id = Column(String)
    subject = Column(String)
    content = Column(Text)
    is_read = Column(Boolean, default=False)
    sent_at = Column(DateTime, default=datetime.datetime.utcnow)

# 12. Digital Documents
class DigitalDocument(Base):
    __tablename__ = "digital_documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    file_url = Column(String)
    file_type = Column(String)
    file_size_kb = Column(Float)
    category = Column(String)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    is_archived = Column(Boolean, default=False)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

# 14. SMS Notifications
class SMSNotification(Base):
    __tablename__ = "sms_notifications"
    id = Column(Integer, primary_key=True, index=True)
    recipient_phone = Column(String)
    message = Column(Text)
    notification_type = Column(String)  # Inama, Umuganda, Mituweli, Emergency
    sent_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="Sent")

# 15. AI Assistant
class AIChatLog(Base):
    __tablename__ = "ai_chat_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
