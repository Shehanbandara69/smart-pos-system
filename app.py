# Enhanced POS System - Complete Solution for Mobile Accessories & Future Categories
# Built for Streamlit Free Plan with SQLite Database

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit.connections import SQLConnection 
from sqlalchemy import text
import base64
from io import BytesIO
from PIL import Image
import json
import extra_streamlit_components as stx

# ----------------- CONFIGURATION -----------------
st.set_page_config(
    page_title="Smart POS System",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force proper text rendering
st.markdown("""
<script>
    // Force text color in all elements
    document.addEventListener('DOMContentLoaded', function() {
        const style = document.createElement('style');
        style.textContent = `
            * { color: #2d3748 !important; }
            select, option { color: #2d3748 !important; }
        `;
        document.head.appendChild(style);
    });
</script>
""", unsafe_allow_html=True)

# Custom CSS for modern, professional design
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Global styling */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container with gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    
    /* Top bar for user info and logout */
    .top-bar {
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem 2rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .user-info {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2d3748;
    }
    
    /* Card styling with better shadows */
    .stat-card {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin: 0.5rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid rgba(255,255,255,0.5);
    }
    
    .stat-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        border-color: #667eea;
    }
    
    .stat-value {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 0.95rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    /* Product card with modern design */
    .product-card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0.5rem;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .product-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .product-card:hover::before {
        transform: scaleX(1);
    }
    
    .product-card:hover {
        border-color: #667eea;
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    /* Enhanced buttons */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Primary button gradient */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Success banner with animation */
    .success-banner {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
        font-size: 1.1rem;
        animation: slideDown 0.5s ease;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 15px;
        border: none;
        padding: 1.5rem;
        font-weight: 500;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Fix dropdown text visibility - Enhanced */
    .stSelectbox label {
        color: #2d3748 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background-color: white !important;
        min-height: 3rem !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background-color: white !important;
        color: #2d3748 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        padding: 0.75rem !important;
        line-height: 1.5 !important;
    }
    
    /* Fix selected value text */
    .stSelectbox [data-baseweb="select"] [role="button"] {
        color: #2d3748 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    /* Fix dropdown menu items */
    [data-baseweb="popover"] [role="option"] {
        color: #2d3748 !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
    }
    
    /* Fix placeholder text */
    .stSelectbox [data-baseweb="select"] input {
        color: #64748b !important;
    }
    
    /* Alternative fix for select box */
    div[data-baseweb="select"] > div {
        color: #2d3748 !important;
        background-color: white !important;
    }
    
    /* Fix text input labels */
    .stTextInput label, .stNumberInput label {
        color: #2d3748 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
    }
    
    /* Fix textarea labels */
    .stTextArea label {
        color: #2d3748 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Expander text fix */
    .streamlit-expanderHeader {
        color: #2d3748 !important;
        font-weight: 600 !important;
        background-color: white !important;
    }
    
    /* Form labels - catch all */
    label {
        color: #2d3748 !important;
        font-weight: 500 !important;
    }
    
    /* Fix all selectbox content */
    .stSelectbox div[data-baseweb="select"] span {
        color: #2d3748 !important;
    }
    
    /* Force text color in select */
    select, .stSelectbox * {
        color: #2d3748 !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 12px;
        font-weight: 600;
        color: #2d3748;
        padding: 1rem;
        border: 2px solid #e2e8f0;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #667eea;
        background: #f7fafc;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        font-weight: 600;
        background: rgba(255,255,255,0.7);
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        border-color: #667eea;
        border-bottom-color: white;
    }
    
    /* Form styling */
    .stForm {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid #e2e8f0;
    }
    
    /* Cart styling */
    .cart-item {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 2px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    
    .cart-item:hover {
        border-color: #667eea;
        background: white;
    }
    
    /* Metric styling */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #e2e8f0;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Login page styling */
    .login-container {
        background: white;
        padding: 3rem;
        border-radius: 25px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin-top: 5rem;
    }
    
    .login-title {
        text-align: center;
        color: #667eea;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .login-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Charts */
    .stPlotlyChart, .stLineChart, .stBarChart {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5568d3 0%, #6d4391 100%);
    }
    
    /* Toast/Success message */
    .element-container:has(.success-banner) {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 999;
        animation: slideInRight 0.5s ease;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
        }
        to {
            transform: translateX(0);
        }
    }
    
    /* Loading animation */
    .stSpinner > div {
        border-color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- AUTHENTICATION DATA -----------------
try:
    ADMIN_PASS = st.secrets["user_credentials"]["admin_password"]
    CASHIER_PIN = st.secrets["user_credentials"]["cashier_pin"]
except KeyError:
    st.error("🔴 ERROR: user_credentials not found in .streamlit/secrets.toml")
    st.stop()

# Initialize Cookie Manager (without cache to avoid widget warning)
def get_cookie_manager():
    return stx.CookieManager()

cookie_manager = get_cookie_manager()

# State Initialization
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'cart' not in st.session_state:
    st.session_state['cart'] = []
if 'remember_me' not in st.session_state:
    st.session_state['remember_me'] = False
if 'auth_checked' not in st.session_state:
    st.session_state['auth_checked'] = False
if 'login_mode' not in st.session_state:
    st.session_state['login_mode'] = None

# ----------------- DATABASE CONNECTION & SETUP -----------------

@st.cache_resource
def setup_database():
    """Initialize database with all required tables - Using persistent storage for Streamlit Cloud"""
    try:
        # Use Streamlit's persistent storage path if available (for cloud deployment)
        # Falls back to local path for development
        import os
        
        # Check if running on Streamlit Cloud
        if os.path.exists("/mount/src"):
            # Streamlit Cloud persistent storage
            db_path = "/mount/src/pos_system.db"
        else:
            # Local development
            db_path = "pos_system.db"
        
        # Create connection string
        connection_string = f"sqlite:///{db_path}"
        
        conn = st.connection("sqlite", type=SQLConnection, url=connection_string)
        
        with conn.session as session:
            # Categories Table
            session.execute(text("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    created_at TEXT
                )
            """))
            
            # Products/Inventory Table
            session.execute(text("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category_id INTEGER,
                    description TEXT,
                    cost_price REAL,
                    selling_price REAL,
                    stock_quantity INTEGER DEFAULT 0,
                    image_data TEXT,
                    barcode TEXT,
                    created_at TEXT,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            """))
            
            # Transactions Table
            session.execute(text("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_id TEXT UNIQUE,
                    timestamp TEXT,
                    customer_name TEXT,
                    customer_phone TEXT,
                    subtotal REAL,
                    discount_amount REAL,
                    discount_percentage REAL,
                    tax_amount REAL,
                    total_amount REAL,
                    payment_method TEXT,
                    served_by TEXT
                )
            """))
            
            # Transaction Items Table
            session.execute(text("""
                CREATE TABLE IF NOT EXISTS transaction_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_id TEXT,
                    product_id INTEGER,
                    product_name TEXT,
                    quantity INTEGER,
                    unit_price REAL,
                    discount REAL,
                    total REAL,
                    FOREIGN KEY (transaction_id) REFERENCES transactions (transaction_id),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            """))
            
            # Insert default category if none exists
            session.execute(text("""
                INSERT OR IGNORE INTO categories (name, description, created_at) 
                VALUES ('Mobile Accessories', 'Phone cases, chargers, cables, screen protectors', :created_at)
            """), {"created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            
            session.commit()  # Commit all table creation and initial data
        
        # Store db path in session state for backup feature
        st.session_state['db_path'] = db_path
            
        return conn
    except Exception as e:
        st.error(f"🔴 DATABASE CONNECTION FAILED: {e}")
        st.stop()

# ----------------- HELPER FUNCTIONS -----------------

def generate_transaction_id():
    """Generate unique transaction ID"""
    return f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}"

def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def base64_to_image(base64_string):
    """Convert base64 string to PIL Image"""
    if base64_string:
        image_data = base64.b64decode(base64_string)
        return Image.open(BytesIO(image_data))
    return None

# ----------------- DATA OPERATIONS -----------------

@st.cache_data(ttl=300)
def load_categories(_conn):
    """Load all categories"""
    try:
        df = _conn.query("SELECT * FROM categories ORDER BY name")
        return df
    except:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_products(_conn):
    """Load all products with category names"""
    try:
        df = _conn.query("""
            SELECT p.*, c.name as category_name 
            FROM products p 
            LEFT JOIN categories c ON p.category_id = c.id 
            ORDER BY p.name
        """)
        return df
    except:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_transactions(_conn, days=30):
    """Load transactions from last N days"""
    try:
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        df = _conn.query(f"""
            SELECT * FROM transactions 
            WHERE timestamp >= '{start_date}' 
            ORDER BY timestamp DESC
        """)
        return df
    except:
        return pd.DataFrame()

def add_category(conn, name, description):
    """Add new category"""
    try:
        with conn.session as session:
            session.execute(text("""
                INSERT INTO categories (name, description, created_at) 
                VALUES (:name, :description, :created_at)
            """), {
                "name": name,
                "description": description,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            session.commit()  # Commit the transaction
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error adding category: {e}")
        return False

def add_product(conn, name, category_id, description, cost_price, selling_price, stock, image_data, barcode):
    """Add new product"""
    try:
        with conn.session as session:
            session.execute(text("""
                INSERT INTO products (name, category_id, description, cost_price, selling_price, 
                                    stock_quantity, image_data, barcode, created_at) 
                VALUES (:name, :category_id, :description, :cost_price, :selling_price, 
                        :stock, :image_data, :barcode, :created_at)
            """), {
                "name": name,
                "category_id": category_id,
                "description": description,
                "cost_price": cost_price,
                "selling_price": selling_price,
                "stock": stock,
                "image_data": image_data,
                "barcode": barcode,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            session.commit()  # Commit the transaction
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error adding product: {e}")
        return False

def update_product_stock(conn, product_id, quantity_change):
    """Update product stock"""
    try:
        with conn.session as session:
            session.execute(text("""
                UPDATE products 
                SET stock_quantity = stock_quantity + :change 
                WHERE id = :product_id
            """), {"product_id": product_id, "change": quantity_change})
            session.commit()  # Commit the transaction
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error updating stock: {e}")
        return False

def save_transaction(conn, transaction_data, items):
    """Save complete transaction with stock validation"""
    try:
        with conn.session as session:
            # First, verify stock availability for all items
            for item in items:
                result = session.execute(text("""
                    SELECT stock_quantity FROM products WHERE id = :product_id
                """), {"product_id": item["product_id"]})
                
                current_stock = result.fetchone()
                if current_stock is None:
                    raise ValueError(f"Product {item['product_name']} not found")
                
                if current_stock[0] < item["quantity"]:
                    raise ValueError(f"Insufficient stock for {item['product_name']}. Available: {current_stock[0]}, Requested: {item['quantity']}")
            
            # If all stock checks pass, proceed with transaction
            # Save transaction header
            session.execute(text("""
                INSERT INTO transactions (transaction_id, timestamp, customer_name, customer_phone,
                                        subtotal, discount_amount, discount_percentage, tax_amount,
                                        total_amount, payment_method, served_by)
                VALUES (:txn_id, :timestamp, :customer_name, :customer_phone, :subtotal,
                        :discount_amount, :discount_percentage, :tax_amount, :total_amount,
                        :payment_method, :served_by)
            """), transaction_data)
            
            # Save transaction items and update stock
            for item in items:
                session.execute(text("""
                    INSERT INTO transaction_items (transaction_id, product_id, product_name,
                                                  quantity, unit_price, discount, total)
                    VALUES (:txn_id, :product_id, :product_name, :quantity, :unit_price,
                            :discount, :total)
                """), item)
                
                # Update stock - this will never go negative due to check above
                session.execute(text("""
                    UPDATE products 
                    SET stock_quantity = stock_quantity - :quantity 
                    WHERE id = :product_id AND stock_quantity >= :quantity
                """), {"product_id": item["product_id"], "quantity": item["quantity"]})
            
            session.commit()  # Commit all changes
        
        st.cache_data.clear()
        return True
    except ValueError as ve:
        st.error(f"Stock validation error: {ve}")
        return False
    except Exception as e:
        st.error(f"Error saving transaction: {e}")
        return False

# ----------------- AUTHENTICATION -----------------

def login_user(username, password):
    """Authenticate user"""
    if username == "admin" and password == ADMIN_PASS:
        return "Admin"
    elif username == "cashier" and password == CASHIER_PIN:
        return "Cashier"
    return None

def logout():
    """Logout user and return to appropriate screen"""
    st.session_state['logged_in'] = False
    st.session_state['user_role'] = None
    st.session_state['username'] = None
    st.session_state['cart'] = []
    st.session_state['remember_me'] = False
    
    # Clear cookies with unique keys
    cookie_manager.delete('pos_username', key='logout_del_username')
    cookie_manager.delete('pos_role', key='logout_del_role')
    cookie_manager.delete('pos_remember', key='logout_del_remember')
    
    # Clear admin parameter and return to cashier interface
    st.query_params.clear()
    
    st.success("✅ Logged out successfully!")
    st.rerun()

# ----------------- UI COMPONENTS -----------------

def show_top_bar(context="main"):
    """Display top bar with user info and logout button"""
    col1, col2 = st.columns([4, 1])
    
    with col1:
        role_emoji = "👨‍💼" if st.session_state['user_role'] == "Admin" else "💰"
        st.markdown(f"""
            <div class="top-bar">
                <div class="user-info">
                    {role_emoji} Welcome, <strong>{st.session_state['user_role']}</strong> 
                    {f"({st.session_state['username']})" if st.session_state['username'] else ""}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", key=f"logout_btn_{context}", type="primary", use_container_width=True):
            logout()

def show_stat_card(label, value, icon="📊"):
    """Display a statistic card"""
    st.markdown(f"""
        <div class="stat-card">
            <p class="stat-label">{icon} {label}</p>
            <p class="stat-value">{value}</p>
        </div>
    """, unsafe_allow_html=True)

def show_success_message(message):
    """Show animated success message"""
    st.markdown(f"""
        <div class="success-banner">
            ✅ {message}
        </div>
    """, unsafe_allow_html=True)
    st.balloons()

def show_sale_history(conn, limit=10):
    """Display recent sale history"""
    st.subheader("📋 Recent Sales History")
    
    try:
        # Load recent transactions
        transactions = conn.query(f"""
            SELECT 
                transaction_id,
                timestamp,
                customer_name,
                total_amount,
                payment_method,
                served_by
            FROM transactions 
            ORDER BY timestamp DESC 
            LIMIT {limit}
        """)
        
        if transactions.empty:
            st.info("No sales history yet. Complete your first sale to see it here!")
            return
        
        # Format the data
        transactions['timestamp'] = pd.to_datetime(transactions['timestamp'])
        transactions['Date'] = transactions['timestamp'].dt.strftime('%Y-%m-%d')
        transactions['Time'] = transactions['timestamp'].dt.strftime('%H:%M:%S')
        transactions['Amount'] = transactions['total_amount'].apply(lambda x: f"Rs {x:,.2f}")
        
        # Display in expandable cards
        for _, txn in transactions.iterrows():
            with st.expander(f"🧾 {txn['transaction_id']} - {txn['Date']} {txn['Time']} - {txn['Amount']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Transaction ID:** {txn['transaction_id']}")
                    st.write(f"**Date:** {txn['Date']}")
                    st.write(f"**Time:** {txn['Time']}")
                    
                with col2:
                    st.write(f"**Total Amount:** {txn['Amount']}")
                    st.write(f"**Payment Method:** {txn['payment_method']}")
                    st.write(f"**Served By:** {txn['served_by']}")
                    if txn['customer_name']:
                        st.write(f"**Customer:** {txn['customer_name']}")
                
                # Get transaction items
                items = conn.query(f"""
                    SELECT product_name, quantity, unit_price, total
                    FROM transaction_items 
                    WHERE transaction_id = '{txn['transaction_id']}'
                """)
                
                if not items.empty:
                    st.markdown("**Items Sold:**")
                    items['Unit Price'] = items['unit_price'].apply(lambda x: f"Rs {x:,.2f}")
                    items['Total'] = items['total'].apply(lambda x: f"Rs {x:,.2f}")
                    items_display = items[['product_name', 'quantity', 'Unit Price', 'Total']]
                    items_display.columns = ['Product', 'Qty', 'Unit Price', 'Total']
                    st.dataframe(items_display, use_container_width=True, hide_index=True)
        
        # Show summary
        st.divider()
        total_sales = transactions['total_amount'].sum()
        st.info(f"💰 **Total Sales (Last {len(transactions)} transactions):** Rs {total_sales:,.2f}")
        
    except Exception as e:
        st.error(f"Error loading sale history: {e}")

def category_management(conn):
    """Category management interface"""
    st.subheader("📁 Category Management")
    
    # Display existing categories
    categories = load_categories(conn)
    if not categories.empty:
        st.dataframe(categories[['name', 'description']], use_container_width=True, hide_index=True)
    
    # Add new category
    with st.expander("➕ Add New Category"):
        with st.form("add_category_form"):
            cat_name = st.text_input("Category Name*")
            cat_desc = st.text_area("Description")
            submitted = st.form_submit_button("Add Category", type="primary")
            
            if submitted and cat_name:
                if add_category(conn, cat_name, cat_desc):
                    show_success_message(f"Category '{cat_name}' added successfully!")
                    st.rerun()

def inventory_management(conn):
    """Complete inventory management"""
    st.subheader("📦 Inventory Management")
    
    tab1, tab2 = st.tabs(["📋 View Products", "➕ Add Product"])
    
    with tab1:
        products = load_products(conn)
        if not products.empty:
            # Search and filter
            col1, col2 = st.columns([3, 1])
            with col1:
                search = st.text_input("🔍 Search products", "", key="inventory_search")
            with col2:
                categories = load_categories(conn)
                cat_filter = st.selectbox("Filter by Category", ["All"] + categories['name'].tolist(), key="inventory_category_filter")
            
            # Filter products
            filtered = products.copy()
            if search:
                filtered = filtered[filtered['name'].str.contains(search, case=False, na=False)]
            if cat_filter != "All":
                filtered = filtered[filtered['category_name'] == cat_filter]
            
            # Display products
            for _, product in filtered.iterrows():
                with st.expander(f"**{product['name']}** - Stock: {product['stock_quantity']} - Rs {product['selling_price']:,.2f}"):
                    col1, col2, col3 = st.columns([1, 2, 1])
                    
                    with col1:
                        if product['image_data']:
                            img = base64_to_image(product['image_data'])
                            st.image(img, use_container_width=True)
                    
                    with col2:
                        st.write(f"**Category:** {product['category_name']}")
                        st.write(f"**Description:** {product['description']}")
                        st.write(f"**Cost Price:** Rs {product['cost_price']:,.2f}")
                        st.write(f"**Selling Price:** Rs {product['selling_price']:,.2f}")
                        st.write(f"**Profit Margin:** Rs {product['selling_price'] - product['cost_price']:,.2f}")
                        if product['barcode']:
                            st.write(f"**Barcode:** {product['barcode']}")
                    
                    with col3:
                        st.metric("Current Stock", product['stock_quantity'])
                        stock_change = st.number_input("Adjust Stock", min_value=-1000, max_value=1000, 
                                                      value=0, key=f"stock_{product['id']}")
                        if st.button("Update", key=f"update_{product['id']}"):
                            if update_product_stock(conn, product['id'], stock_change):
                                show_success_message("Stock updated successfully!")
                                st.rerun()
        else:
            st.info("No products in inventory. Add your first product!")
    
    with tab2:
        categories = load_categories(conn)
        if categories.empty:
            st.warning("Please add at least one category first!")
            return
        
        with st.form("add_product_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                prod_name = st.text_input("Product Name*")
                category = st.selectbox("Category*", categories['id'].tolist(), 
                                       format_func=lambda x: categories[categories['id']==x]['name'].iloc[0])
                description = st.text_area("Description")
                barcode = st.text_input("Barcode/SKU")
            
            with col2:
                cost_price = st.number_input("Cost Price (Rs)*", min_value=0.0, format="%.2f")
                selling_price = st.number_input("Selling Price (Rs)*", min_value=0.0, format="%.2f")
                initial_stock = st.number_input("Initial Stock*", min_value=0, value=0)
                
                if selling_price > 0 and cost_price > 0:
                    profit = selling_price - cost_price
                    margin = (profit / selling_price) * 100
                    st.info(f"💰 Profit: Rs {profit:.2f} ({margin:.1f}%)")
            
            uploaded_image = st.file_uploader("Product Image", type=['png', 'jpg', 'jpeg'])
            
            submitted = st.form_submit_button("Add Product", type="primary")
            
            if submitted:
                if not prod_name or selling_price <= 0:
                    st.error("Please fill all required fields!")
                else:
                    image_data = None
                    if uploaded_image:
                        img = Image.open(uploaded_image)
                        img.thumbnail((400, 400))
                        image_data = image_to_base64(img)
                    
                    if add_product(conn, prod_name, category, description, cost_price, 
                                 selling_price, initial_stock, image_data, barcode):
                        show_success_message(f"Product '{prod_name}' added successfully!")
                        st.rerun()

def cashier_terminal_content(conn):
    """Cashier terminal content without top bar - for embedding in admin dashboard"""
    # Load products
    products = load_products(conn)
    
    if products.empty:
        st.warning("⚠️ No products available. Please add products in Admin panel.")
        return
    
    # Main layout
    col_products, col_cart = st.columns([3, 2])
    
    with col_products:
        st.subheader("🛍️ Products")
        
        # Search and category filter
        search = st.text_input("🔍 Search products", key="search_products_embedded")
        categories = load_categories(conn)
        cat_filter = st.selectbox("Category", ["All"] + categories['name'].tolist(), key="cat_filter_embedded")
        
        # Filter products
        filtered = products[products['stock_quantity'] > 0].copy()
        if search:
            filtered = filtered[filtered['name'].str.contains(search, case=False, na=False)]
        if cat_filter != "All":
            filtered = filtered[filtered['category_name'] == cat_filter]
        
        # Display products in a grid
        cols = st.columns(3)
        for idx, (_, product) in enumerate(filtered.iterrows()):
            with cols[idx % 3]:
                with st.container():
                    if product['image_data']:
                        img = base64_to_image(product['image_data'])
                        st.image(img, use_container_width=True)
                    
                    st.markdown(f"**{product['name']}**")
                    st.caption(f"Rs {product['selling_price']:,.2f}")
                    
                    # Show stock with color coding
                    stock_qty = product['stock_quantity']
                    if stock_qty == 0:
                        st.caption("⛔ Out of Stock")
                    elif stock_qty < 5:
                        st.caption(f"⚠️ Low Stock: {stock_qty}")
                    else:
                        st.caption(f"✅ Stock: {stock_qty}")
                    
                    # Calculate how many already in cart
                    in_cart = sum(item['quantity'] for item in st.session_state['cart'] if item['id'] == product['id'])
                    available_to_add = stock_qty - in_cart
                    
                    if stock_qty == 0:
                        st.button("❌ Out of Stock", key=f"add_embedded_{product['id']}", disabled=True, use_container_width=True)
                    elif available_to_add <= 0:
                        st.button("⚠️ Max in Cart", key=f"add_embedded_{product['id']}", disabled=True, use_container_width=True)
                    else:
                        if st.button("➕ Add", key=f"add_embedded_{product['id']}", use_container_width=True):
                            st.session_state['cart'].append({
                                'id': product['id'],
                                'name': product['name'],
                                'price': product['selling_price'],
                                'quantity': 1,
                                'max_stock': stock_qty
                            })
                            st.rerun()
    
    with col_cart:
        st.subheader("🛒 Cart")
        
        if not st.session_state['cart']:
            st.info("Cart is empty. Add products to start.")
        else:
            # Display cart items
            subtotal = 0
            stock_warning = False
            
            for idx, item in enumerate(st.session_state['cart']):
                # Get current stock from database
                product_stock = products[products['id'] == item['id']]['stock_quantity'].values
                max_qty = product_stock[0] if len(product_stock) > 0 else 1
                
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    st.write(item['name'])
                    # Show stock warning if quantity exceeds available
                    if item['quantity'] > max_qty:
                        st.caption(f"⚠️ Only {max_qty} in stock")
                        stock_warning = True
                        
                with col2:
                    qty = st.number_input(
                        "Qty", 
                        min_value=1, 
                        max_value=int(max_qty),
                        value=min(item['quantity'], int(max_qty)), 
                        key=f"qty_embedded_{idx}", 
                        label_visibility="collapsed"
                    )
                    st.session_state['cart'][idx]['quantity'] = qty
                    
                with col3:
                    st.write(f"Rs {item['price'] * qty:,.2f}")
                with col4:
                    if st.button("🗑️", key=f"del_embedded_{idx}"):
                        st.session_state['cart'].pop(idx)
                        st.rerun()
                
                subtotal += item['price'] * qty
            
            # Show warning if stock issues
            if stock_warning:
                st.warning("⚠️ Some items have been adjusted to match available stock")
            
            st.divider()
            
            # Discount
            discount_type = st.radio("Discount Type", ["None", "Percentage", "Fixed Amount"], horizontal=True, key="discount_type_radio_embedded")
            discount_value = 0
            discount_amount = 0
            
            if discount_type == "Percentage":
                discount_value = st.slider("Discount %", 0, 100, 0, key="discount_percentage_slider_embedded")
                discount_amount = subtotal * (discount_value / 100)
            elif discount_type == "Fixed Amount":
                discount_amount = st.number_input("Discount Amount (Rs)", min_value=0.0, max_value=float(subtotal), key="discount_amount_input_embedded")
                discount_value = (discount_amount / subtotal * 100) if subtotal > 0 else 0
            
            # Calculate totals
            tax_rate = 0  # You can add tax if needed
            tax_amount = 0
            total = subtotal - discount_amount + tax_amount
            
            # Display totals
            st.markdown(f"**Subtotal:** Rs {subtotal:,.2f}")
            if discount_amount > 0:
                st.markdown(f"**Discount:** -Rs {discount_amount:,.2f}")
            st.markdown(f"### **Total:** Rs {total:,.2f}")
            
            # Customer details
            with st.expander("Customer Details (Optional)"):
                customer_name = st.text_input("Name", key="customer_name_input_embedded")
                customer_phone = st.text_input("Phone", key="customer_phone_input_embedded")
            
            payment_method = st.selectbox("Payment Method", ["Cash", "Card", "Mobile Payment", "Other"], key="payment_method_select_embedded")
            
            # Checkout
            if st.button("💳 Complete Sale", key="complete_sale_btn_embedded", type="primary", use_container_width=True):
                # Final stock validation before sale
                stock_error = False
                error_messages = []
                
                for item in st.session_state['cart']:
                    product_stock = products[products['id'] == item['id']]['stock_quantity'].values
                    if len(product_stock) > 0:
                        available_stock = product_stock[0]
                        if item['quantity'] > available_stock:
                            stock_error = True
                            error_messages.append(f"❌ {item['name']}: Only {available_stock} available (you have {item['quantity']} in cart)")
                
                if stock_error:
                    st.error("Cannot complete sale - Insufficient stock!")
                    for msg in error_messages:
                        st.error(msg)
                    st.info("💡 Please adjust quantities in cart or remove items")
                else:
                    # Prepare transaction data
                    txn_id = generate_transaction_id()
                    transaction_data = {
                        "txn_id": txn_id,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "customer_name": customer_name if 'customer_name' in locals() else "",
                        "customer_phone": customer_phone if 'customer_phone' in locals() else "",
                        "subtotal": subtotal,
                        "discount_amount": discount_amount,
                        "discount_percentage": discount_value,
                        "tax_amount": tax_amount,
                        "total_amount": total,
                        "payment_method": payment_method,
                        "served_by": st.session_state['user_role']
                    }
                    
                    # Prepare items
                    items = []
                    for item in st.session_state['cart']:
                        items.append({
                            "txn_id": txn_id,
                            "product_id": item['id'],
                            "product_name": item['name'],
                            "quantity": item['quantity'],
                            "unit_price": item['price'],
                            "discount": 0,
                            "total": item['price'] * item['quantity']
                        })
                    
                    # Save transaction
                    if save_transaction(conn, transaction_data, items):
                        show_success_message(f"Sale completed! Transaction ID: {txn_id}")
                        st.session_state['cart'] = []
                        st.rerun()
            
            if st.button("🗑️ Clear Cart", key="clear_cart_btn_embedded", use_container_width=True):
                st.session_state['cart'] = []
                st.rerun()

def cashier_terminal(conn):
    """Modern cashier interface with cart - standalone version"""
    st.title("💰 Cashier Terminal")
    
    # Show top bar with logout
    show_top_bar(context="cashier")
    
    # Tab navigation for cashier
    tab1, tab2 = st.tabs(["🛒 Make Sale", "📋 Sale History"])
    
    with tab1:
        # Show the cashier content
        cashier_terminal_content(conn)
    
    with tab2:
        # Show sale history for cashier
        show_sale_history(conn, limit=20)

def cashier_terminal_direct(conn):
    """Direct cashier access - no login required"""
    st.title("💰 POS - Sales Terminal")
    
    # Show admin access button in corner
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("🔐 Admin", key="admin_access_btn", use_container_width=True):
            # Redirect to admin login
            st.query_params["admin"] = "true"
            st.rerun()
    
    # Tab navigation for cashier
    tab1, tab2 = st.tabs(["🛒 Make Sale", "📋 Sale History"])
    
    with tab1:
        # Show the cashier content
        cashier_terminal_content(conn)
    
    with tab2:
        # Show sale history for cashier
        show_sale_history(conn, limit=20)

def admin_login_view():
    """Simple admin login - only for admin access"""
    st.title("🔐 Admin Access")
    
    # Back to cashier button
    if st.button("⬅️ Back to Cashier", use_container_width=False):
        # Clear admin parameter
        st.query_params.clear()
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 20px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
        """, unsafe_allow_html=True)
        
        with st.form("admin_login_form"):
            st.markdown("### 👨‍💼 Admin Login")
            
            username = st.text_input("Username", placeholder="admin", key="admin_username")
            password = st.text_input("Password", type="password", placeholder="Enter password", key="admin_password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button("🚀 Login", type="primary", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.error("❌ Please enter username and password")
                else:
                    role = login_user(username, password)
                    if role == "Admin":
                        st.session_state['logged_in'] = True
                        st.session_state['user_role'] = role
                        st.session_state['username'] = username
                        
                        st.success("✅ Login Successful!")
                        import time
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("❌ Invalid admin credentials")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.expander("ℹ️ Admin Credentials"):
            st.markdown("""
                **Default Admin:**
                - Username: `admin`
                - Password: `admin123`
            """)

def sales_reports(conn):
    """Comprehensive sales reports and analytics"""
    st.subheader("📊 Sales Reports & Analytics")
    
    # Date range selector
    col1, col2, col3 = st.columns(3)
    with col1:
        report_period = st.selectbox("Report Period", 
                                     ["Today", "Last 7 Days", "Last 30 Days", "Last 90 Days", "Custom"],
                                     key="report_period_select")
    
    if report_period == "Custom":
        with col2:
            start_date = st.date_input("Start Date", key="report_start_date")
        with col3:
            end_date = st.date_input("End Date", key="report_end_date")
    else:
        days_map = {"Today": 1, "Last 7 Days": 7, "Last 30 Days": 30, "Last 90 Days": 90}
        days = days_map[report_period]
        end_date = datetime.now().date()
        start_date = (datetime.now() - timedelta(days=days)).date()
    
    # Load data
    transactions = load_transactions(conn, days=365)
    if not transactions.empty:
        transactions['timestamp'] = pd.to_datetime(transactions['timestamp'])
        transactions = transactions[
            (transactions['timestamp'].dt.date >= start_date) & 
            (transactions['timestamp'].dt.date <= end_date)
        ]
    
    if transactions.empty:
        st.info("No transactions found for the selected period.")
        return
    
    # Summary metrics
    st.markdown("### 📈 Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        show_stat_card("Total Sales", f"Rs {transactions['total_amount'].sum():,.2f}", "💰")
    with col2:
        show_stat_card("Transactions", f"{len(transactions)}", "🧾")
    with col3:
        show_stat_card("Avg Sale", f"Rs {transactions['total_amount'].mean():,.2f}", "📊")
    with col4:
        show_stat_card("Discounts Given", f"Rs {transactions['discount_amount'].sum():,.2f}", "🎫")
    
    # Charts
    st.markdown("### 📉 Trends")
    
    # Daily sales chart
    daily_sales = transactions.groupby(transactions['timestamp'].dt.date)['total_amount'].sum().reset_index()
    daily_sales.columns = ['Date', 'Sales']
    st.line_chart(daily_sales.set_index('Date'))
    
    # Payment method breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Payment Methods")
        payment_summary = transactions.groupby('payment_method')['total_amount'].sum().reset_index()
        st.bar_chart(payment_summary.set_index('payment_method'))
    
    with col2:
        st.markdown("#### Top Products")
        # Load transaction items
        items_df = conn.query(f"""
            SELECT product_name, SUM(quantity) as total_qty, SUM(total) as total_sales
            FROM transaction_items 
            WHERE transaction_id IN (SELECT transaction_id FROM transactions 
                                    WHERE timestamp >= '{start_date}' AND timestamp <= '{end_date}')
            GROUP BY product_name 
            ORDER BY total_sales DESC 
            LIMIT 10
        """)
        if not items_df.empty:
            st.dataframe(items_df, use_container_width=True, hide_index=True)
    
    # Detailed transactions
    st.markdown("### 📋 Transaction Details")
    st.dataframe(
        transactions[['transaction_id', 'timestamp', 'customer_name', 'total_amount', 'payment_method']],
        use_container_width=True,
        hide_index=True
    )

def admin_dashboard(conn):
    """Complete admin dashboard"""
    st.title("🎛️ Admin Dashboard")
    
    # Show top bar with logout
    show_top_bar(context="admin")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "📦 Inventory", 
        "📁 Categories", 
        "💰 Sales", 
        "📈 Reports"
    ])
    
    with tab1:
        # Dashboard overview
        st.markdown("### Quick Stats")
        
        products = load_products(conn)
        transactions = load_transactions(conn, 30)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_products = len(products) if not products.empty else 0
            show_stat_card("Total Products", total_products, "📦")
        
        with col2:
            low_stock = len(products[products['stock_quantity'] < 10]) if not products.empty else 0
            show_stat_card("Low Stock Items", low_stock, "⚠️")
        
        with col3:
            total_sales = transactions['total_amount'].sum() if not transactions.empty else 0
            show_stat_card("Sales (30 Days)", f"Rs {total_sales:,.2f}", "💰")
        
        with col4:
            total_txn = len(transactions) if not transactions.empty else 0
            show_stat_card("Transactions", total_txn, "🧾")
        
        # Low stock alert
        if not products.empty and low_stock > 0:
            st.warning(f"⚠️ {low_stock} products have low stock (< 10 units)")
            low_stock_items = products[products['stock_quantity'] < 10][['name', 'stock_quantity', 'category_name']]
            st.dataframe(low_stock_items, use_container_width=True, hide_index=True)
        
        # Database Backup Section
        st.markdown("---")
        st.markdown("### 💾 Database Backup")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info("📦 **Backup your database regularly to prevent data loss!**\n\n"
                   "The backup includes all:\n"
                   "- Products & Inventory\n"
                   "- Categories\n"
                   "- Transactions & Sales History\n"
                   "- All system data")
        
        with col2:
            if st.button("⬇️ Download Database Backup", type="primary", use_container_width=True):
                try:
                    from pathlib import Path
                    
                    # Get database path from session state
                    db_path = st.session_state.get('db_path', 'pos_system.db')
                    
                    if Path(db_path).exists():
                        # Read database file
                        with open(db_path, 'rb') as f:
                            db_data = f.read()
                        
                        # Create download button
                        backup_filename = f"pos_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                        
                        st.download_button(
                            label="💾 Click to Download",
                            data=db_data,
                            file_name=backup_filename,
                            mime="application/octet-stream",
                            use_container_width=True,
                            key="db_download_btn"
                        )
                        
                        st.success(f"✅ Backup ready! Click button above to download.")
                        st.caption(f"📁 Database location: `{db_path}`")
                    else:
                        st.error(f"❌ Database file not found at: {db_path}")
                        
                except Exception as e:
                    st.error(f"❌ Backup failed: {e}")
            
            st.caption("💡 Tip: Download backups daily or before major changes")
    
    with tab2:
        inventory_management(conn)
    
    with tab3:
        category_management(conn)
    
    with tab4:
        # Sales tab with sub-tabs
        sales_tab1, sales_tab2 = st.tabs(["💳 Point of Sale", "📋 Recent Sales"])
        
        with sales_tab1:
            cashier_terminal_content(conn)
        
        with sales_tab2:
            show_sale_history(conn, limit=50)
    
    with tab5:
        sales_reports(conn)

# ----------------- LOGIN VIEW -----------------

def login_view():
    """Modern login interface with separate Admin/Cashier buttons"""
    
    # Check cookies for auto-login (ONLY for cashier, only once per session)
    if not st.session_state.get('auth_checked'):
        st.session_state['auth_checked'] = True
        
        # Get cookies
        all_cookies = cookie_manager.get_all()
        
        if all_cookies and 'pos_remember' in all_cookies:
            remember = all_cookies.get('pos_remember')
            
            if remember == 'true':
                saved_username = all_cookies.get('pos_username')
                saved_role = all_cookies.get('pos_role')
                
                # Only auto-login for Cashier, not Admin
                if saved_username and saved_role and saved_role == "Cashier":
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = saved_role
                    st.session_state['username'] = saved_username
                    st.session_state['remember_me'] = True
                    st.rerun()
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Login card
        st.markdown("""
            <div class="login-container">
                <div class="login-title">🛍️ Smart POS</div>
                <div class="login-subtitle">Mobile Accessories & More</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Quick Access Buttons
        st.markdown("### Quick Access")
        col_admin, col_cashier = st.columns(2)
        
        with col_admin:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 15px; text-align: center; margin-bottom: 1rem;'>
                    <h3 style='color: white; margin: 0;'>👨‍💼 Admin</h3>
                    <p style='color: rgba(255,255,255,0.8); font-size: 0.9rem; margin: 0.5rem 0;'>
                        Full System Access
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔐 Admin Login", key="quick_admin_btn", use_container_width=True, type="primary"):
                st.session_state['login_mode'] = 'admin'
        
        with col_cashier:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                padding: 1.5rem; border-radius: 15px; text-align: center; margin-bottom: 1rem;'>
                    <h3 style='color: white; margin: 0;'>💰 Cashier</h3>
                    <p style='color: rgba(255,255,255,0.8); font-size: 0.9rem; margin: 0.5rem 0;'>
                        Sales Terminal Only
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Cashier Login", key="quick_cashier_btn", use_container_width=True):
                st.session_state['login_mode'] = 'cashier'
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Show login form only if mode is selected
        if st.session_state.get('login_mode'):
            login_mode = st.session_state['login_mode']
            
            # Login form with white background
            with st.container():
                st.markdown("""
                    <div style='background: white; padding: 2rem; border-radius: 20px; 
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
                """, unsafe_allow_html=True)
                
                with st.form("login_form", clear_on_submit=False):
                    if login_mode == 'admin':
                        st.markdown("### 👨‍💼 Admin Login")
                        username_label = "Admin Username"
                        password_label = "Admin Password"
                        expected_username = "admin"
                        show_remember = False  # Admin must login manually each time
                    else:
                        st.markdown("### 💰 Cashier Login")
                        username_label = "Cashier Username"
                        password_label = "Cashier PIN"
                        expected_username = "cashier"
                        show_remember = True  # Cashier can use auto-login
                    
                    # Get saved username from cookies (only for cashier)
                    all_cookies = cookie_manager.get_all()
                    default_username = ''
                    default_remember = False
                    
                    if login_mode == 'cashier' and all_cookies:
                        default_username = all_cookies.get('pos_username', '')
                        default_remember = all_cookies.get('pos_remember', 'false') == 'true'
                    
                    username = st.text_input(
                        username_label, 
                        value=default_username,
                        placeholder=expected_username,
                        key="login_username"
                    )
                    
                    password = st.text_input(
                        password_label, 
                        type="password", 
                        placeholder="Enter password/PIN",
                        key="login_password"
                    )
                    
                    # Remember me checkbox (only for cashier)
                    if show_remember:
                        remember = st.checkbox(
                            "🔒 Keep me logged in (auto-login on refresh)", 
                            value=default_remember,
                            key="remember_checkbox"
                        )
                    else:
                        remember = False
                        st.info("🔐 Admin must login manually each time for security")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    col_a, col_b, col_c = st.columns([1, 1, 1])
                    with col_a:
                        submitted = st.form_submit_button(
                            "🚀 Login", 
                            type="primary", 
                            use_container_width=True
                        )
                    with col_b:
                        back_btn = st.form_submit_button(
                            "⬅️ Back",
                            use_container_width=True
                        )
                    with col_c:
                        if show_remember:
                            clear_btn = st.form_submit_button(
                                "🔄 Clear",
                                use_container_width=True
                            )
                        else:
                            clear_btn = False
                    
                    if back_btn:
                        st.session_state['login_mode'] = None
                        st.rerun()
                    
                    if clear_btn and show_remember:
                        # Clear cookies with unique keys
                        cookie_manager.delete('pos_username', key='clear_del_username')
                        cookie_manager.delete('pos_role', key='clear_del_role')
                        cookie_manager.delete('pos_remember', key='clear_del_remember')
                        st.session_state['username'] = None
                        st.session_state['remember_me'] = False
                        st.rerun()
                    
                    if submitted:
                        if not username or not password:
                            st.error("❌ Please enter both username and password")
                        else:
                            role = login_user(username, password)
                            
                            # Validate role matches login mode
                            if role and ((login_mode == 'admin' and role == 'Admin') or (login_mode == 'cashier' and role == 'Cashier')):
                                st.session_state['logged_in'] = True
                                st.session_state['user_role'] = role
                                st.session_state['username'] = username
                                st.session_state['remember_me'] = remember
                                
                                # Save to cookies ONLY if cashier and remember me is checked
                                if remember and role == "Cashier":
                                    # Cookies expire in 30 days
                                    cookie_manager.set('pos_username', username, key='set_username_cookie', expires_at=datetime.now() + timedelta(days=30))
                                    cookie_manager.set('pos_role', role, key='set_role_cookie', expires_at=datetime.now() + timedelta(days=30))
                                    cookie_manager.set('pos_remember', 'true', key='set_remember_cookie', expires_at=datetime.now() + timedelta(days=30))
                                else:
                                    # Clear cookies for admin or if not remembering
                                    cookie_manager.delete('pos_username', key='del_username_cookie')
                                    cookie_manager.delete('pos_role', key='del_role_cookie')
                                    cookie_manager.delete('pos_remember', key='del_remember_cookie')
                                
                                # Show success message
                                st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                                    color: white; padding: 1rem; border-radius: 10px; text-align: center;
                                    font-weight: 600; margin-top: 1rem;'>
                                        ✅ Login Successful! Welcome {role}
                                    </div>
                                """, unsafe_allow_html=True)
                                
                                # Redirect after short delay
                                import time
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error(f"❌ Invalid credentials for {login_mode} login")
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Info card
        with st.expander("ℹ️ Demo Credentials & Info", expanded=False):
            st.markdown("""
                **Admin Access (Manual Login Only):**
                - Username: `admin`
                - Password: `admin123`
                - Full system access
                - Must login each time (no auto-login for security)
                
                **Cashier Access (Can Auto-Login):**
                - Username: `cashier`
                - Password: `0000`
                - Sales terminal only
                - Can enable "Keep me logged in" for convenience
                
                **💡 Security Tips:**
                - Admins always login manually for security
                - Cashiers can use auto-login on trusted devices
                - Always logout when leaving the device
            """)
        
        # Footer
        st.markdown("""
            <div style='text-align: center; color: white; margin-top: 2rem; opacity: 0.8;'>
                <small>Powered by Streamlit • Secure & Fast</small>
            </div>
        """, unsafe_allow_html=True)

# ----------------- MAIN APP -----------------

def main():
    """Main application logic - Auto-open Cashier, Admin via URL"""
    conn = setup_database()
    
    # Check for admin access via URL parameter
    # Access admin by adding ?admin=true to URL
    query_params = st.query_params
    
    if "admin" in query_params:
        # Admin mode - show login
        if not st.session_state['logged_in'] or st.session_state['user_role'] != 'Admin':
            admin_login_view()
        else:
            admin_dashboard(conn)
    else:
        # Default: Direct cashier interface (no login needed)
        cashier_terminal_direct(conn)

if __name__ == "__main__":
    main()