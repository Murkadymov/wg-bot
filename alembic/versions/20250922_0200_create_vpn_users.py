from alembic import op

# revision identifiers, used by Alembic.
revision = "20250922_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE vpn_users (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL UNIQUE,
            username TEXT,
            full_name TEXT,
            public_key TEXT NOT NULL,
            ip_address TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT now()
        );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE vpn_users;")
