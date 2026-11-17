// Minimal JSON parser/serializer for the exercise judge (C++17).
#pragma once
#include <cctype>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

struct Json {
    enum Type { NUL, BOOL, NUM, STR, ARR, OBJ } type = NUL;
    bool b = false;
    double num = 0;
    std::string str;
    std::vector<Json> arr;
    std::map<std::string, Json> obj;

    static Json mk_null() { return Json(); }
    static Json mk_bool(bool v) { Json j; j.type = BOOL; j.b = v; return j; }
    static Json mk_num(double v) { Json j; j.type = NUM; j.num = v; return j; }
    static Json mk_str(const std::string& v) { Json j; j.type = STR; j.str = v; return j; }
    static Json mk_arr(std::vector<Json> v) { Json j; j.type = ARR; j.arr = std::move(v); return j; }
    static Json mk_obj() { Json j; j.type = OBJ; return j; }

    bool is_null() const { return type == NUL; }
    bool as_bool() const { return b; }
    double as_double() const { return num; }
    long long as_long() const { return (long long)llround(num); }
    const std::string& as_string() const { return str; }
    const std::vector<Json>& as_array() const { return arr; }
    bool has(const std::string& k) const { return obj.count(k) > 0; }
    const Json& at(const std::string& k) const {
        auto it = obj.find(k);
        if (it == obj.end()) throw std::runtime_error("missing key: " + k);
        return it->second;
    }
    void set(const std::string& k, Json v) { type = OBJ; obj[k] = std::move(v); }

    std::string dump() const {
        std::ostringstream os;
        write(os);
        return os.str();
    }

    static Json parse(const std::string& s) {
        size_t i = 0;
        Json j = parse_value(s, i);
        skip_ws(s, i);
        return j;
    }

private:
    void write(std::ostringstream& os) const {
        switch (type) {
        case NUL: os << "null"; break;
        case BOOL: os << (b ? "true" : "false"); break;
        case NUM:
            if (std::isfinite(num) && num == std::floor(num) && std::fabs(num) < 9e15) {
                os << (long long)num;
            } else {
                os.precision(17);
                os << num;
            }
            break;
        case STR: write_str(os, str); break;
        case ARR: {
            os << '[';
            for (size_t i = 0; i < arr.size(); i++) {
                if (i) os << ',';
                arr[i].write(os);
            }
            os << ']';
            break;
        }
        case OBJ: {
            os << '{';
            bool first = true;
            for (const auto& kv : obj) {
                if (!first) os << ',';
                first = false;
                write_str(os, kv.first);
                os << ':';
                kv.second.write(os);
            }
            os << '}';
            break;
        }
        }
    }

    static void write_str(std::ostringstream& os, const std::string& s) {
        os << '"';
        for (unsigned char c : s) {
            switch (c) {
            case '"': os << "\\\""; break;
            case '\\': os << "\\\\"; break;
            case '\n': os << "\\n"; break;
            case '\r': os << "\\r"; break;
            case '\t': os << "\\t"; break;
            case '\b': os << "\\b"; break;
            case '\f': os << "\\f"; break;
            default:
                if (c < 0x20) {
                    char buf[8];
                    snprintf(buf, sizeof(buf), "\\u%04x", c);
                    os << buf;
                } else {
                    os << c;
                }
            }
        }
        os << '"';
    }

    static void skip_ws(const std::string& s, size_t& i) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
    }
    static char peek(const std::string& s, size_t i) {
        if (i >= s.size()) throw std::runtime_error("unexpected end of json");
        return s[i];
    }

    static Json parse_value(const std::string& s, size_t& i) {
        skip_ws(s, i);
        char c = peek(s, i);
        if (c == '{') return parse_obj(s, i);
        if (c == '[') return parse_arr(s, i);
        if (c == '"') return mk_str(parse_str(s, i));
        if (c == 't') { expect(s, i, "true"); return mk_bool(true); }
        if (c == 'f') { expect(s, i, "false"); return mk_bool(false); }
        if (c == 'n') { expect(s, i, "null"); return mk_null(); }
        return parse_num(s, i);
    }
    static void expect(const std::string& s, size_t& i, const char* lit) {
        for (const char* p = lit; *p; p++, i++) {
            if (i >= s.size() || s[i] != *p) throw std::runtime_error("bad json literal");
        }
    }
    static Json parse_num(const std::string& s, size_t& i) {
        size_t start = i;
        if (peek(s, i) == '-') i++;
        while (i < s.size() && (isdigit((unsigned char)s[i]) || s[i] == '.' ||
               s[i] == 'e' || s[i] == 'E' || s[i] == '+' || s[i] == '-')) i++;
        if (i == start) throw std::runtime_error("bad json number");
        return mk_num(strtod(s.substr(start, i - start).c_str(), nullptr));
    }
    static std::string parse_str(const std::string& s, size_t& i) {
        if (peek(s, i) != '"') throw std::runtime_error("expected string");
        i++;
        std::string out;
        while (true) {
            char c = peek(s, i);
            i++;
            if (c == '"') break;
            if (c == '\\') {
                char e = peek(s, i);
                i++;
                switch (e) {
                case '"': out += '"'; break;
                case '\\': out += '\\'; break;
                case '/': out += '/'; break;
                case 'b': out += '\b'; break;
                case 'f': out += '\f'; break;
                case 'n': out += '\n'; break;
                case 'r': out += '\r'; break;
                case 't': out += '\t'; break;
                case 'u': {
                    unsigned cp = parse_hex4(s, i);
                    if (cp >= 0xD800 && cp <= 0xDBFF && i + 1 < s.size() &&
                        s[i] == '\\' && s[i + 1] == 'u') {
                        i += 2;
                        unsigned lo = parse_hex4(s, i);
                        cp = 0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00);
                    }
                    append_utf8(out, cp);
                    break;
                }
                default: throw std::runtime_error("bad escape");
                }
            } else {
                out += c;
            }
        }
        return out;
    }
    static unsigned parse_hex4(const std::string& s, size_t& i) {
        unsigned v = 0;
        for (int k = 0; k < 4; k++) {
            char c = peek(s, i);
            i++;
            v <<= 4;
            if (c >= '0' && c <= '9') v |= c - '0';
            else if (c >= 'a' && c <= 'f') v |= c - 'a' + 10;
            else if (c >= 'A' && c <= 'F') v |= c - 'A' + 10;
            else throw std::runtime_error("bad hex");
        }
        return v;
    }
    static void append_utf8(std::string& out, unsigned cp) {
        if (cp < 0x80) {
            out += (char)cp;
        } else if (cp < 0x800) {
            out += (char)(0xC0 | (cp >> 6));
            out += (char)(0x80 | (cp & 0x3F));
        } else if (cp < 0x10000) {
            out += (char)(0xE0 | (cp >> 12));
            out += (char)(0x80 | ((cp >> 6) & 0x3F));
            out += (char)(0x80 | (cp & 0x3F));
        } else {
            out += (char)(0xF0 | (cp >> 18));
            out += (char)(0x80 | ((cp >> 12) & 0x3F));
            out += (char)(0x80 | ((cp >> 6) & 0x3F));
            out += (char)(0x80 | (cp & 0x3F));
        }
    }
    static Json parse_arr(const std::string& s, size_t& i) {
        i++; // [
        std::vector<Json> out;
        skip_ws(s, i);
        if (peek(s, i) == ']') { i++; return mk_arr(out); }
        while (true) {
            out.push_back(parse_value(s, i));
            skip_ws(s, i);
            char c = peek(s, i);
            i++;
            if (c == ']') break;
            if (c != ',') throw std::runtime_error("expected , or ]");
        }
        return mk_arr(out);
    }
    static Json parse_obj(const std::string& s, size_t& i) {
        i++; // {
        Json out = mk_obj();
        skip_ws(s, i);
        if (peek(s, i) == '}') { i++; return out; }
        while (true) {
            skip_ws(s, i);
            std::string k = parse_str(s, i);
            skip_ws(s, i);
            if (peek(s, i) != ':') throw std::runtime_error("expected :");
            i++;
            out.set(k, parse_value(s, i));
            skip_ws(s, i);
            char c = peek(s, i);
            i++;
            if (c == '}') break;
            if (c != ',') throw std::runtime_error("expected , or }");
        }
        return out;
    }
};