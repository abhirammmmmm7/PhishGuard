from urllib.parse import urlparse
import re


def extract_features(url, feature_columns):
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path
    query = parsed.query

    features = {}

    # ---------- BASIC URL FEATURES ----------
    features["length_url"] = len(url)
    features["length_hostname"] = len(domain)

    # ---------- URL CHARACTER COUNTS ----------
    features["qty_dot_url"] = url.count(".")
    features["qty_hyphen_url"] = url.count("-")
    features["qty_slash_url"] = url.count("/")
    features["qty_questionmark_url"] = url.count("?")
    features["qty_equal_url"] = url.count("=")
    features["qty_at_url"] = url.count("@")
    features["qty_and_url"] = url.count("&")
    features["qty_exclamation_url"] = url.count("!")
    features["qty_space_url"] = url.count(" ")

    # ---------- DOMAIN FEATURES ----------
    features["qty_dot_domain"] = domain.count(".")
    features["qty_hyphen_domain"] = domain.count("-")
    features["qty_vowels_domain"] = sum(domain.count(v) for v in "aeiou")

    # ---------- PATH FEATURES ----------
    features["qty_slash_path"] = path.count("/")
    features["qty_dot_path"] = path.count(".")
    features["length_path"] = len(path)

    # ---------- QUERY FEATURES ----------
    features["length_query"] = len(query)
    features["qty_params"] = query.count("&") + 1 if query else 0

    # ---------- IP ADDRESS ----------
    features["qty_ip_resolved"] = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", domain) else 0

    # ---------- HTTPS ----------
    features["tls_ssl_certificate"] = 1 if parsed.scheme == "https" else 0

    # ---------- SUSPICIOUS KEYWORDS ----------
    suspicious_words = ["login", "secure", "verify", "account", "update", "bank"]
    features["qty_sensitive_words"] = sum(word in url.lower() for word in suspicious_words)

    # ---------- FINAL ALIGNMENT ----------
    # Fill missing features with 0 (VERY IMPORTANT)
    final_features = {
        col: features.get(col, 0)
        for col in feature_columns
    }

    return final_features
